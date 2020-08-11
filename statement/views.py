import json
import jwt
import requests

from datetime import (
    datetime,
    timedelta
)

from django.shortcuts import render
from django.views     import View
from django.http      import (
    JsonResponse,
    HttpResponse
)

from statement.models import (
    PersonalStatement, 
    StatementList
)

from account.utils    import decorator_login

from account.models   import (
    User, 
    Applicant, 
    Corrector
)

from my_settings      import SECRET


class StatementWrite(View):
    @decorator_login
    def post(self, request):
        user_input_data = json.loads(request.body)
        user_input      = user_input_data['dataArr']
        received_user   = request.user
        statement_list  = user_input['statement']
        if Applicant.objects.filter(user=received_user).exists():

            personal_statement = PersonalStatement.objects.create(
                applicant               = Applicant.objects.get(user=received_user),
                company                 = user_input['company'],
                job_position            = user_input['job_position'],
                is_answer_completed     = user_input['is_completed'],
                is_correction_completed = False
            )

            for statement in statement_list:
                StatementList(
                    statement            = personal_statement, 
                    statement_question   = statement['question'],
                    statement_answer     = statement['answer'],
                    statement_correction = statement['answer'],
                    order                = statement['id'],
                ).save()

        else:
            Applicant.objects.create(user=received_user)

            personal_statement = PersonalStatement.objects.create(
                applicant               = Applicant.objects.get(user=received_user),
                company                 = user_input['company'],
                job_position            = user_input['job_position'],
                is_answer_completed     = user_input['is_completed'],
                is_correction_completed = False
            )

            for statement in statement_list:
                StatementList(
                    statement            = personal_statement, 
                    statement_question   = statement['question'],
                    statement_answer     = statement['answer'],
                    statement_correction = statement['answer'],
                    order                = statement['id'],
                ).save()

        return JsonResponse({"message": "save success"}, status=200)

class StatementDetailView(View):
    @decorator_login
    def get(self, request, statement_id):
        specified_statement = PersonalStatement.objects.get(id=statement_id)
        user_statements     = StatementList.objects.filter(statement=specified_statement)        
        statement_list=[
                        {
                        "statement_id" : statement.id,   
                        "id"           : statement.order,
                        "question"     : statement.statement_question,
                        "correction"   : statement.statement_correction,
                        "comment"      : statement.statement_comment,
                        "answer"       : statement.statement_answer
                        }
                        for statement in user_statements]
            
        return JsonResponse({"statement": statement_list,"specified_id":specified_statement.id}, status=200)


class StatementListView(View):
    @decorator_login
    def get(self, request):
        received_user = request.user

        if received_user.is_corrector==True:

            submitted_statements = PersonalStatement.objects.filter(is_answer_completed=1)
            statement_list=[
                            {
                            "id"                  : statement.id,  
                            "applicant_name"      : statement.applicant.user.name,   
                            "applicant_thumbnail" : statement.applicant.user.profile_thumbnail,   
                            "corrector_name"      : '고양이',   
                            "corrector_thumbnail" : 'https://i.pinimg.com/564x/fb/fa/b5/fbfab5595b2edb76f4aa574999ca52d7.jpg',   
                            "apply_company"       : statement.company,
                            "apply_job_position"  : statement.job_position,
                            "submitted_date"      : statement.updated_at,
                            "is_answer_completed" : statement.is_answer_completed,
                            "is_corrected"        : statement.is_correction_completed
                            }
                            for statement in submitted_statements]
                    
        elif received_user.is_corrector==False:

            submitted_statements = PersonalStatement.objects.filter(applicant=Applicant.objects.get(user=received_user))
            statement_list=[
                            {
                            "id"                  : statement.id,  
                            "applicant_name"      : statement.applicant.user.name,   
                            "applicant_thumbnail" : statement.applicant.user.profile_thumbnail,   
                            "corrector_name"      : '고양이',   
                            "corrector_thumbnail" : 'https://i.pinimg.com/564x/fb/fa/b5/fbfab5595b2edb76f4aa574999ca52d7.jpg',  
                            "apply_company"       : statement.company,
                            "apply_job_position"  : statement.job_position,
                            "submitted_date"      : statement.updated_at,
                            "is_answer_completed" : statement.is_answer_completed,                            
                            "is_corrected"        : statement.is_correction_completed
                            }
                            for statement in submitted_statements]


        return JsonResponse({"statement": statement_list}, status=200)


class CorrectionUpdateView(View):
    def kakao_message_send(self, access_token, name, company, job_position):
        template_dict_data = str({
                        "object_type": "text",
                        "text": f"{name}님, {company} {job_position}직무 자기소개서 첨삭이 완료되었습니다",
                        "link": {
                            "web_url": "https://developers.kakao.com",
                            "mobile_web_url": "https://developers.kakao.com"
                        },
                        "button_title": "바로 확인"
                    } 
        )

        template_json_data = "template_object=" + str(json.dumps(template_dict_data))   

        template_json_data = template_json_data.replace("\"", "")
        template_json_data = template_json_data.replace("'", "\"")

        kakao_request = requests.request(
            method="POST",
            url="https://kapi.kakao.com/v2/api/talk/memo/default/send",
            headers = {
                "Host"          : "kapi.kakao.com",
                "Authorization" : f"Bearer {access_token}",
                "Content-type"  : "application/x-www-form-urlencoded"
            },
            data=template_json_data)
        
        return JsonResponse({"message":"1"},status = kakao_request.status_code)

    def post(self, request):
        user_input_data = json.loads(request.body)
        user_input      = user_input_data["revisionArr"]
        
        correction_list = user_input
        
        for correction in correction_list:
            user_statement = StatementList.objects.get(id=correction['statement_id'])

            if correction["correction"] != None:
                user_statement.statement_correction=correction["correction"]
            if correction["comment"] != None:
                user_statement.statement_comment=correction["comment"]

            user_statement.save()

        if user_input_data['is_completed'] == 1:   
            personal_statement = PersonalStatement.objects.get(id=StatementList.objects.get(id=user_input[0]['statement_id']).statement_id)
            personal_statement.is_correction_completed = True
            personal_statement.save()

            self.kakao_message_send(
                access_token=user_input['applicant_token'], 
                name=personal_statement.applicant.user.name, 
                company=personal_statement.company, 
                job_position=personal_statement.job_position
                )

        return JsonResponse({"message": "save success"}, status=200)
    

class CorrectionResultView(View):
    @decorator_login
    def get(self, request, statement_id):
        received_user = request.user
        specified_statement = PersonalStatement.objects.get(id=statement_id)
        user_statements = StatementList.objects.filter(statement=specified_statement)        
        statement_list=[
                        {
                        "statement_id" : statement.id,   
                        "id"           : statement.order,
                        "question"     : statement.statement_question,
                        "answer"       : statement.statement_answer,
                        "correction"   : statement.statement_correction,
                        "comment"      : statement.statement_comment,
                        }
                        for statement in user_statements]       
        return JsonResponse({"statement": statement_list}, status=200)

