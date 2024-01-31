from app.utils.arequest import arequest
import copy, re, os
from app.utils.mongo import BaseModel

hotel_model = BaseModel('hotel')
class HotelRepository:    
    def __get_address(self, acme_hotel, patagonia_hotel, paperflies_hotel):
        patagonia_hotel_address = patagonia_hotel.get('address')
        paperflies_hotel_address = paperflies_hotel.get('location', {}).get('address')
        # Use paperflies first because it seem not missing any address and correct address compare to acme
        if paperflies_hotel_address is not None:
            return paperflies_hotel_address
        if patagonia_hotel_address is not None: 
            return patagonia_hotel_address
        if acme_hotel.get('Address', '') != '' and acme_hotel.get('PostalCode', '') != '':
            return acme_hotel.get('Address').strip() + ', ' + acme_hotel.get('PostalCode').strip()
        return None
        

    def __get_by_priority(self, first_priority_field, second_priority_field = None, third_priority_field = None):
        if first_priority_field is not None and first_priority_field != '': 
            return first_priority_field
        if second_priority_field is not None and second_priority_field != '': 
            return second_priority_field
        if third_priority_field is not None and third_priority_field != '': 
            return third_priority_field
        return None

    def __unique_image_link(self, data_images):
        result = []
        unique_link = set()
        for r in data_images: 
            link = r.get('link', r.get('url'))
            description = r.get('caption', r.get('description'))
            if link is None or link in unique_link: continue
            result.append({ 'link': link, 'description': description })
            unique_link.add(link)

        return result

    def __get_image(self, patagonia_hotel, paperflies_hotel):
        default_image = {
            'rooms': [],
            'site': [],
            'amenities': []
        }
        result = copy.deepcopy(default_image)
        result['rooms'] = self.__unique_image_link(patagonia_hotel.get('images', default_image)['rooms'] + paperflies_hotel.get('images', default_image)['rooms'])
        result['site'] = self.__unique_image_link(paperflies_hotel.get('images', default_image)['site'])
        result['amenities'] = self.__unique_image_link(patagonia_hotel.get('images', default_image)['amenities'])

        return result

    def __get_amenities(self, acme_hotel, patagonia_hotel, paperflies_hotel): 
        default_amenities = { 
            'general': [],
            'room': []
        }
        result = {
            'general': paperflies_hotel.get('amenities', default_amenities).get('general', []),
            'room': paperflies_hotel.get('amenities', default_amenities).get('room', []),
        }
        general_type = ['outdoor pool', 'indoor pool', 'pool', 'business center', 'childcare', 'parking', 'bar', 'dry cleaning', 'wifi', 'breakfast', 'concierge']
        room_type = ['aircon', 'minibar', 'tv', 'bathtub', 'tub', 'hair dryer', 'coffee machine', 'kettle', 'iron']

        acme_amenities = []
        if acme_hotel.get('Facilities', []) is not None:
            acme_amenities = acme_hotel.get('Facilities', [])

        patagonia_amenities = []
        if patagonia_hotel.get('amenities', []) is not None:
            patagonia_amenities = patagonia_hotel.get('amenities', [])

        acme_patagonia_amenities = acme_amenities + patagonia_amenities
        for a in acme_patagonia_amenities:
            a = a.strip()
            # Except case
            if a.lower() == 'wifi':
                result['general'].append(a.lower())
                continue
            # Convert camel case to standard
            a = re.sub(r'([a-z])([A-Z])', r'\1 \2', a).lower()
            if a in general_type:
                result['general'].append(a)
            elif a in room_type:
                result['room'].append(a)
            else: 
                continue
            # @Todo Other case if data is expand

        # Unique field result
        result['room'] = list(set(result['room']))
        result['general'] = list(set(result['general']))
        return result

    async def __get_hotel_by_suppliers(self, hotel_ids = [], destination_id = None):
        acme_hotel = await arequest.get(os.getenv('ACME_URL'))
        patagonia_hotel = await arequest.get(os.getenv('PATAGONIA_URL'))
        paperflies_hotel = await arequest.get(os.getenv('PAPERFLIES_URL'))
    
        acme_hotel = acme_hotel if acme_hotel is not None else []
        patagonia_hotel = patagonia_hotel if patagonia_hotel is not None else []
        paperflies_hotel = paperflies_hotel if paperflies_hotel is not None else []

        if len(hotel_ids) > 0:
            acme_hotel = [h for h in acme_hotel if h['Id'] in hotel_ids]
            patagonia_hotel = [h for h in patagonia_hotel if h['id'] in hotel_ids]
            paperflies_hotel = [h for h in paperflies_hotel if h['hotel_id'] in hotel_ids]

            # @Todo: Handle case if len(hotel) > 1 then log to check the supplier

            
        if destination_id is not None:
            acme_hotel = [h for h in acme_hotel if h['DestinationId'] == destination_id]
            patagonia_hotel = [h for h in patagonia_hotel if h['destination'] == destination_id]
            paperflies_hotel = [h for h in paperflies_hotel if h['destination_id'] == destination_id]

        unique_hotel_ids = set([h['Id'] for h in acme_hotel] + [h['id'] for h in patagonia_hotel]  + [h['hotel_id'] for h in paperflies_hotel])
        
        result = []
        for id in unique_hotel_ids:
            found_acme_hotel = next((h for h in acme_hotel if h['Id'] == id), {})
            found_patagonia_hotel = next((h for h in patagonia_hotel if h['id'] == id), {})
            found_paperflies_hotel = next((h for h in paperflies_hotel if h['hotel_id'] == id), {})

            hotel_detail = {
                'id': id,
                # Dont care the priority for destination, name
                'destination_id': self.__get_by_priority(found_acme_hotel.get('DestinationId'), found_patagonia_hotel.get('destination'), found_paperflies_hotel.get('destination_id')),
                'name': self.__get_by_priority(found_acme_hotel.get('Name'), found_patagonia_hotel.get('name'), found_paperflies_hotel.get('hotel_name')),
                'location': {
                    # Lat lng prefer patagonia because it not missing or empty string data than acme
                    'lat': self.__get_by_priority(found_patagonia_hotel.get('lat'), found_acme_hotel.get('Latitude')),
                    'lng': self.__get_by_priority(found_patagonia_hotel.get('lng'), found_acme_hotel.get('Longitude')),
                    'address': self.__get_address(found_acme_hotel, found_patagonia_hotel, found_paperflies_hotel),
                    'city': found_acme_hotel.get('City'),
                    'country': self.__get_by_priority(found_paperflies_hotel.get('location', {}).get('country'), found_acme_hotel.get('Country'))
                },
                # Description prefer paperflies hotel > patagonia > acme
                'description': self.__get_by_priority(found_paperflies_hotel.get('details'), found_patagonia_hotel.get('info'), found_acme_hotel.get('Description')),
                'images': self.__get_image(found_patagonia_hotel, found_paperflies_hotel),
                'amenities': self.__get_amenities(found_acme_hotel, found_patagonia_hotel, found_paperflies_hotel),
                'booking_conditions': found_paperflies_hotel.get('booking_conditions', [])
            }

            result.append(hotel_detail)
        return result

    async def get_hotels(self, hotel_ids = [], destination_id = None):
        if not len(hotel_ids) and not destination_id: return []
        condition = {}
        if len(hotel_ids):
            condition['id'] = { '$in': hotel_ids }
        if destination_id is not None:
            condition['destination_id'] = destination_id

        results = await hotel_model.get_all_by_condition(condition)
        if results is None or not len(results):
            results = await self.__get_hotel_by_suppliers(hotel_ids, destination_id)
            if len(results):
                await hotel_model.save_many(results)

        for r in results:
            r.pop('_id', None)


        return results
    
    async def init_fetch_all_hotels(self):
        all_hotels = await self.__get_hotel_by_suppliers()
        if len(all_hotels):
                await hotel_model.save_many(all_hotels)

