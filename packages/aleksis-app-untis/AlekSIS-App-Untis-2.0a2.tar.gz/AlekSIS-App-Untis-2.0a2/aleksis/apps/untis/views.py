from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from rules.contrib.views import permission_required

from aleksis.core.models import Group

from .forms import GroupSubjectFormset, UntisUploadForm
from .util.xml.xml import untis_import_xml


@permission_required("untis.do_xml_import")
def xml_import(request: HttpRequest) -> HttpResponse:
    context = {}

    upload_form = UntisUploadForm()

    if request.method == "POST":
        upload_form = UntisUploadForm(request.POST, request.FILES)

        if upload_form.is_valid():
            untis_import_xml(request, request.FILES["untis_xml"])

    context["upload_form"] = upload_form

    return render(request, "untis/xml_import.html", context)


@permission_required("untis.assign_subjects_to_groups")
def groups_subjects(request: HttpRequest) -> HttpResponse:
    """Assign subjects to groups (for matching by MySQL importer)."""
    context = {}

    groups_qs = Group.objects.all()

    # Paginate
    paginator = Paginator(groups_qs, 100)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    groups_paged = groups_qs.filter(id__in=[g.id for g in page])

    # Create filtered queryset
    group_subject_formset = GroupSubjectFormset(request.POST or None, queryset=groups_paged)

    # Check if form is submitted and valid, then save
    if request.method == "POST":
        if group_subject_formset.is_valid():
            group_subject_formset.save()
            messages.success(request, _("Your changes were successfully saved."))

    context["formset"] = group_subject_formset
    context["page"] = page
    context["paginator"] = paginator

    return render(request, "untis/groups_subjects.html", context)
