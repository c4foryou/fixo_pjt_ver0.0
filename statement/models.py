from django.db import models

class PersonalStatement(models.Model):
    applicant               = models.ForeignKey('account.Applicant', on_delete=models.CASCADE, null = True)
    corrector               = models.ForeignKey('account.Corrector', on_delete=models.CASCADE, null = True)
    company                 = models.CharField(max_length = 50, null = True)
    job_position            = models.CharField(max_length = 50, null = True)
    is_answer_completed     = models.BooleanField(null = True)
    is_correction_completed = models.BooleanField(null = True)    
    created_at              = models.DateTimeField(auto_now_add = True)
    updated_at              = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'personal_statements'

class StatementList(models.Model):
    statement = models.ForeignKey('PersonalStatement', on_delete=models.CASCADE, null = True)
    statement_question      = models.TextField(max_length = 50000, null = True)
    statement_answer        = models.TextField(max_length = 50000, null = True)
    statement_correction    = models.TextField(max_length = 50000, null = True)
    statement_comment       = models.TextField(max_length = 50000, null = True)
    order                   = models.IntegerField(null = True)

    class Meta:
        db_table = 'statement_lists'