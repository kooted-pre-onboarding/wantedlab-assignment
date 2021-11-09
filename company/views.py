import json

from itertools    import permutations
from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models      import Company, RelatedCompany, Tag, Language

class CompanyView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            related_company = []
            with transaction.atomic():
                for language in data['company_name']:
                    languages, created = Language.objects.get_or_create(name=language)
                    company            = Company.objects.create(
                        name = data['company_name'][language]
                    )
                    related_company.append(company.id)
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

                related_company_list = permutations(related_company, 2)
                
                [RelatedCompany.objects.create(
                    company_id         = company_id[0],
                    related_company_id = company_id[1]
                ) for company_id in related_company_list]

            x_wanted_language = request.headers.get("x-wanted-language")
            
            if x_wanted_language not in data['company_name']:
                x_wanted_language = list(data['company_name'].keys())[0]

            company_list      = {
                'company_name' : data['company_name'][x_wanted_language],
                'tags'         : [tag['tag_name'][x_wanted_language] for tag in data['tags']]
            }
            
            return JsonResponse(company_list, status = 201)
        
        except KeyError:
            JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
            
            
