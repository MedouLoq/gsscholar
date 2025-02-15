"""
URL configuration for gestion_schlarite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gs_scholar import views
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    ### users
     path('register/', user_views.register, name='register'),
     path('register1/', user_views.register1, name='register'),
     path('registerstaff/', user_views.registerstaff, name='registers'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.LoginView.as_view(template_name ="users/login.html"), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name ="users/logout.html"), name='logout'),
        path('password-reset/',auth_views.PasswordResetView.as_view(template_name ="users/password_reset.html",html_email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name ="users/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name ="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name ="users/password_reset_complete.html"), name='password_reset_complete'),
    ###
    path('admin/', admin.site.urls),

    path('update_module/<int:id>/', views.update_module, name='update_module'),
    path('delete_module/<int:id>/', views.delete_module, name='delete_module'),
    path('add_module/', views.add_module, name='add_module'),
    path('Module_table/', views.Prof_table, name='Module_table'),
    path('update_matier/<int:id>/', views.update_matier, name='update_matier'),
    path('delete_matier/<int:id>/', views.delete_matier, name='delete_matier'),
    path('import_matiere/', views.import_matiere, name='import_matiere'),
    path('add_matier/', views.add_matier, name='add_matier'),
    path('matier_table/', views.matier_table, name='matier_table'),
    path('prof_table/', views.Prof_table, name='Module_table'),  # Assuming this is your home page
    path('etudiant_table/', views.etudiant_table, name='etudiant_table'),
    path('add_etudiant/', views.add_etudiant, name='add_etudiant'),
    path('update_etudiant/<int:id>/', views.update_etudiant, name='update_etudiant'),
    path('delete_etudiant/<int:Matricul>/', views.delete_etudiant, name='delete_etudiant'),
    path('import_etudiants/', views.import_etudiants, name='import_etudiants'),
    #semester
    path('add_semestre/', views.add_semestre, name='add_semestre'),
    path('update_semestre/<int:id>/', views.update_semestre, name='update_semestre'),
    path('delete_semestre/<int:id>/', views.delete_semestre, name='delete_semestre'),
    path('semestre_table/', views.semestre_table, name='semestre_table'),
    # annee scolaire
    path('add_annee_scolaire/', views.add_annee_scolaire, name='add_annee_scolaire'),
    path('update_annee_scolaire/<int:id>/', views.update_annee_scolaire, name='update_annee_scolaire'),
    path('delete_semestre/<int:id>/', views.delete_semestre, name='delete_semestre'),
    path('annee_scolaire_table/', views.annee_scolaire_table, name='annee_scolaire_table'),
    # niveau
    path('add_niveau/', views.add_niveau, name='add_niveau'),
    path('update_niveau/<int:id>/', views.update_niveau, name='update_niveau'),
    path('delete_niveau/<int:id>/', views.delete_niveau, name='delete_niveau'),
    path('niveau_table/', views.niveau_table, name='niveau_table'),
    path('', views.index, name='index'),

    #questionnaire

    path('questionnaire/<int:questionnaire_id>/', views.QuestionnaireView.as_view(), name='display_questionnaire'),
    path('send_questionnaire_email/', views.SendQuestionnaireEmailView.as_view(), name='send_questionnaire_email'),
    path('mail_sender/', views.mail_sender, name='mail_sender'),
    path('mail_sender_json/', views.mail_sender_json, name='mail_sender_json'),
    path('questionnaire_view/<int:questionnaire_id>/', views.questionnaire, name='questionnaire'),
    path('questionnaire_table/', views.questionnaire_table, name='questionnaire_table'),
    path('update_questionnaire/<int:id>/', views.update_questionnaire, name='update_questionnaire'),
    path('add_questionnaire/', views.add_questionnaire, name='add_questionnaire'),
    path('delete_questionnaire/<int:id>/', views.delete_questionnaire, name='delete_questionnaire'),
    path('questionnaires/<int:id>', views.questionnaire_list, name='questionnaire_list'),
    path('questionnaires2/', views.questionnaire_list2, name='questionnaire_list2'),
    path('generate_radar_chart/<int:id>/', views.generate_radar_chart, name='generate_radar_chart'),
    path('view_radar_chart/<int:id>/', views.view_radar_chart, name='view_radar_chart'),
    path('generate_bar_chart/<int:semester_id>/', views.generate_bar_chart, name='generate_bar_chart'),
    path('semester_graph/', views.semester_list2, name='semester_graph'),
    path('thanku/', views.stop, name='stop'),
    path('view_bar_chart/<int:id>/', views.view_bar_chart, name='view_bar_chart'),
    path('commentaires/<str:id>', views.commentaires, name='commentaires'),
    path('commentaires_download/<str:id>', views.commentaires_download, name='commentaires_download'),
     path('matier_list/<int:id>', views.matier_list, name='matier_list'),
    path('semester_list/', views.semester_list, name='semester_list'),
    path('semester_list3/', views.semester_list3, name='semester_list3'),
    path('semester_list4/', views.semester_list4, name='semester_list4'),
    path('comment/<int:comment_id>/<str:id>/delete/', views.delete_comment, name='delete_comment'),
    path('students_not_filled_questionnaire/<int:semester_id>/', views.students_not_filled_questionnaire, name='students_not_filled_questionnaire'),
     path('get_matiers_for_semester/<int:semester_id>/', views.get_matiers_for_semester, name='get_matiers_for_semester'),
     path('DownloadAllRadarChartsView/<int:semester_id>/', views.DownloadAllRadarChartsView.as_view(), name='DownloadAllRadarChartsView'),


    # section
    path('sections/', views.SectionListView.as_view(), name='section_list'),
    path('sections/create/', views.SectionCreateView.as_view(), name='section_create'),
    path('sections/<int:pk>/update/', views.SectionUpdateView.as_view(), name='section_update'),
    path('sections/<int:pk>/delete/', views.SectionDeleteView.as_view(), name='section_delete'),

    # question
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),

    # email_table
    path('emailtables/', views.EmailtableListView.as_view(), name='emailtable_list'),
    path('emailtables/create/', views.EmailtableCreateView.as_view(), name='emailtable_create'),
    path('emailtables/<int:pk>/update/', views.EmailtableUpdateView.as_view(), name='emailtable_update'),
    path('emailtables/<int:pk>/delete/', views.EmailtableDeleteView.as_view(), name='emailtable_delete'),


    # datainsert
    path('data-inserted-table/', views.data_inserted_table, name='data_inserted_table'),
    path('student_home/', views.student_home, name='student_home'),

    path('students_not_filled_pdf/<int:semester_id>/', views.students_not_filled_pdf, name='students_not_filled_pdf'),
   ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'gs_scholar.views.custom_404'
handler500 = 'gs_scholar.views.custom_500'
