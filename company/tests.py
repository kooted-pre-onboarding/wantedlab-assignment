import json

from django.test    import TestCase, Client

from company.models import Company, CompanyLanguage, CompanyTag, Language, RelatedCompany, Tag, TagLanguage


class CompanyViewTest(TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_company_name_autocomplete(self):
        """
        1. 회사명 자동완성
        회사명의 일부만 들어가도 검색이 되어야 합니다.
        header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
        """
        client = Client()
        headers={"HTTP_x-wanted-language" : "ko"}
        resp = client.get("/search?query=링크", **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(),
           { 'searched_companies' : [{"company_name": "주식회사 링크드코리아"},
            {"company_name": "스피링크"}],
           })
        
    def test_company_search(self):
        """
    2. 회사 이름으로 회사 검색
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
        client = Client()
        headers = {"HTTP_x-wanted-language" : "ko"}
        resp = client.get("/companies/Wantedlab", **headers)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), 
            {
                "company_name": "원티드랩",
                "tags": [
                    "태그_4",
                    "태그_20",
                    "태그_16",
                ],
            })

        # 검색된 회사가 없는경우 404를 리턴합니다.
        resp = client.get(
            "/companies/없는회사", headers=[("x-wanted-language", "ko")]
        )

        self.assertEqual(resp.status_code, 404)
    
    def test_new_company(self):
        """
        3.  새로운 회사 추가
        새로운 언어(tw)도 같이 추가 될 수 있습니다.
        저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
        """
        client = Client()
        
        data={
                "company_name": {
                    "ko": "라인 프레쉬",
                    "tw": "LINE FRESH",
                    "en": "LINE FRESH",
                },
                "tags": [
                    {
                        "tag_name": {
                            "ko": "태그_1",
                            "tw": "tag_1",
                            "en": "tag_1",
                        }
                    },
                    {
                        "tag_name": {
                            "ko": "태그_8",
                            "tw": "tag_8",
                            "en": "tag_8",
                        }
                    },
                    {
                        "tag_name": {
                            "ko": "태그_15",
                            "tw": "tag_15",
                            "en": "tag_15",
                        }
                    }
                ]
            }
        headers = {"HTTP_x-wanted-language" : "tw"}
        resp = client.post("/companies", json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json(), 
            {
                "company_name": "LINE FRESH",
                "tags": [
                    "tag_1",
                    "tag_8",
                    "tag_15",
                ],
            }
        )