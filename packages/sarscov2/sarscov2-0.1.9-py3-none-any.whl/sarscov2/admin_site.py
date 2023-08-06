from django.contrib.admin import AdminSite as DjangoAdminSite
from django.contrib.sites.shortcuts import get_current_site
from edc_sites.models import SiteProfile


class AdminSite(DjangoAdminSite):

    site_title = "SARS-COV-2"
    site_header = "SARS-COV-2"
    index_title = "SARS-COV-2"
    site_url = "/administration/"

    def each_context(self, request):
        context = super().each_context(request)
        title = SiteProfile.objects.get(site=get_current_site(request)).title
        context.update(global_site=get_current_site(request))
        label = "SARS-COV-2"
        context.update(site_title=label, site_header=label, index_title=label)
        return context


sarscov2_admin = AdminSite(name="sarscov2_admin")
sarscov2_admin.disable_action("delete_selected")
