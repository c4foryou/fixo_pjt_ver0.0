from django.contrib import admin

from django.urls import (
    path,
    include
)

from statement.views import (
	StatementDetailView,
	StatementListView,
	StatementWrite,
	CorrectionResultView,
	CorrectionUpdateView
)

urlpatterns = [
	path('/write', StatementWrite.as_view()),
	path('/view/<slug:statement_id>', StatementDetailView.as_view()),
	path('/list', StatementListView.as_view()),
	path('/correction', CorrectionUpdateView.as_view()),
	path('/result/<slug:statement_id>', CorrectionResultView.as_view())
]
