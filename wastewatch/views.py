from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from . import settings
from django.http import HttpResponseForbidden
from .forms import SubmitReportForm, AdminReportForm
from .models import Report
import mimetypes
import operator
import boto3  #needed by test.py for some reason

def main_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return AdminUserView.as_view()(request)
        else:
            return RegularUserView.as_view()(request)
    else:
        return AnonymousUserView.as_view()(request)

class RegularUserView(LoginRequiredMixin, TemplateView):
    template_name = 'common.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['reports'] = Report.objects.filter(user=self.request.user)
        context['count'] = (Report.objects.filter(user=self.request.user).count()
                            - Report.objects.filter(user=self.request.user, status=2).count())
        return context

class AdminUserView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['reports'] = sorted(Report.objects.all(), reverse=True, key=operator.attrgetter('date'))
        context['new'] = Report.objects.filter(status=0).count()
        context['progress'] = Report.objects.filter(status=1).count()
        return context

class AnonymousUserView(TemplateView):
    template_name = 'anonymous.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def logout(request):
    auth_logout(request)
    return main_page(request)


def submit_report(request):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    google_maps_map_id = settings.GOOGLE_MAPS_MAP_ID
    if request.method == 'POST':
        form = SubmitReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            date = form.cleaned_data['date']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            report.date = date
            report.latitude = latitude
            report.longitude = longitude
            '''
            if a file was uploaded, use mimetypes to determine the file type
            '''
            if 'file' in request.FILES:

                uploaded_file = form.cleaned_data['file']
                mime_type = mimetypes.guess_type(uploaded_file.name)[0]
                if mime_type in ['text/plain', 'application/pdf']:
                    report.text_file = uploaded_file
                elif mime_type in ['image/jpeg', 'image/png']:
                    report.image_file = uploaded_file
            if request.user.is_authenticated:
                report.user = request.user
            report.save()
            return redirect('upload_success')
    else:
        form = SubmitReportForm()

    context = {'form': form,
               'google_maps_api_key': google_maps_api_key,
               'google_maps_map_id': google_maps_map_id}
    return render(request, 'report.html', context)

def report_success(request):
    return render(request, 'report_success.html')

def view_report(request, question_id):
    report = get_object_or_404(Report, pk=question_id)
    if not request.user.is_staff:
        return HttpResponseForbidden("Sorry, you don't have permission to view this report")
    if request.method == 'POST':
        form = AdminReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_resolved_success')
    form = AdminReportForm(instance=report)
    if report.status == 0:
        report.status = 1
        report.save()

    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    google_maps_map_id = settings.GOOGLE_MAPS_MAP_ID
    context = {'form': form, 'report': report, 'google_maps_api_key': google_maps_api_key,
               'google_maps_map_id': google_maps_map_id}
    return render(request, 'view_report.html', context)


def report_resolved_success(request):
    return render(request, 'report_resolved_success.html')


def my_reports(request):
    user_reports = Report.objects.filter(user=request.user)
    new = user_reports.filter(status=0).count()
    progress = user_reports.filter(status=1).count()
    total = user_reports.count()

    return render(request, 'my_reports.html', {
        'user_reports': sorted(user_reports, reverse=True, key=operator.attrgetter('date')),
        'new': new,
        'progress': progress,
        'total': total,
    })


def view_my_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    google_maps_map_id = settings.GOOGLE_MAPS_MAP_ID
    context = {'report': report, 'google_maps_api_key': google_maps_api_key,
               'google_maps_map_id': google_maps_map_id}
    return render(request, 'view_my_report.html', context)