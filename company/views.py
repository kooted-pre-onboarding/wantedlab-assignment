import json

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models      import Company, Tag, Language

class CompanyView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                for language in data['company_name']:
                    languages, created = Language.objects.get_or_create(name=language)
                    company            = Company.objects.create(
                        name = data['company_name'][language]
                    )
                    languages.companylanguage_set.create(
                        company = company
                    )
                    for tag in data['tags']:
                        tags, created = Tag.objects.get_or_create(name=tag['tag_name'][language])
                        tags.companytag_set.create(
                            company = company
                        )
                        tags.taglanguage_set.create(
                            language = languages
                        )
                        

            x_wanted_language = request.headers.get("x-wanted-language")
            
            if x_wanted_language not in data['company_name']:
                x_wanted_language = list(data['company_name'].keys())[0]

            company_list      = {
                'company_name' : data['company_name'][x_wanted_language],
                'tags'         : [tag['tag_name'][x_wanted_language] for tag in data['tags']]
            }
            
            return JsonResponse({'result' : company_list}, status = 201)
        
        except KeyError:
            JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
            
            
