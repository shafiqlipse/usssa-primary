from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

"""
Error loading module LVEInfo - Can't locate Cpanel/CPAN/Locale/Maketext/Utils/MarkPhrase.pm in @INC (you may need to install the Cpanel::CPAN::Locale::Maketext::Utils::MarkPhrase module) (@INC contains: /usr/local/cpanel /usr/local/cpanel/whostmgr/docroot/3rdparty/cloudlinux /usr/share/l.v.e-manager/cpanel/cgi /usr/local/cpanel /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux /usr/local/cpanel/3rdparty/perl/536/cpanel-lib /usr/local/cpanel/3rdparty/perl/536/lib/x86_64-linux /usr/local/cpanel/3rdparty/perl/536/lib /opt/cpanel/perl5/536/site_lib/x86_64-linux /opt/cpanel/perl5/536/site_lib) at /usr/local/cpanel/Cpanel/LVEInfo.pm line 20.
BEGIN failed--compilation aborted at /usr/local/cpanel/Cpanel/LVEInfo.pm line 20.
Compilation failed in require at (eval 7) line 1.
BEGIN failed--compilation aborted at (eval 7) line 1.
 at /usr/local/cpanel/Cpanel/LoadModule.pm line 27.
	Cpanel::LoadModule::_logger_warn("Error loading module LVEInfo - Can't locate Cpanel/CPAN/Local"...) called at /usr/local/cpanel/Cpanel/LoadModule.pm line 170
	Cpanel::LoadModule::_modloader("LVEInfo") called at /usr/local/cpanel/Cpanel/LoadModule.pm line 109
	Cpanel::LoadModule::loadmodule("LVEInfo") called at /usr/local/cpanel/Cpanel/Api2/Exec.pm line 44
	Cpanel::Api2::Exec::api2_preexec("LVEInfo", "getLvemanagerVersion") called at /usr/local/cpanel/Cpanel/Template/Plugin/Api2.pm line 204
	Cpanel::Template::Plugin::Api2::_api2_exec("LVEInfo", "getLvemanagerVersion", HASH(0x2f32208)) called at /usr/local/cpanel/base/frontend/jupiter/lveversion/python-selector.html.tt line 2
	eval {...} called at /usr/local/cpanel/base/frontend/jupiter/lveversion/python-selector.html.tt line 2
	eval {...} called at /usr/local/cpanel/base/frontend/jupiter/lveversion/python-selector.html.tt line 7
	Template::Document::__ANON__(Template::Context=HASH(0x2c33d98)) called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template/Document.pm line 165
	eval {...} called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template/Document.pm line 163
	Template::Document::process(Template::Document=HASH(0x2f39798), Template::Context=HASH(0x2c33d98)) called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template/Context.pm line 352
	eval {...} called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template/Context.pm line 322
	Template::Context::process(Template::Context=HASH(0x2c33d98), Template::Document=HASH(0x2f39798)) called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template/Service.pm line 94
	eval {...} called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template/Service.pm line 91
	Template::Service::process(Template::Service=HASH(0x2c33978), "/usr/local/cpanel/base/frontend/jupiter/lveversion/python-sel"..., HASH(0x2c32f18)) called at /usr/local/cpanel/3rdparty/perl/536/cpanel-lib/x86_64-linux/Template.pm line 66
	Template::process(Template=HASH(0x2c335b8), "/usr/local/cpanel/base/frontend/jupiter/lveversion/python-sel"..., HASH(0x2c32f18), SCALAR(0x1d1e968)) called at /usr/local/cpanel/Cpanel/Template.pm line 485
	Cpanel::Template::process_template("cpanel", HASH(0x2c32f18), HASH(0x1d26078)) called at cpanel.pl line 1108
	cpanel::cpanel::cptt_exectag("/usr/local/cpanel/base/frontend/jupiter/lveversion/python-sel"..., 1) called at cpanel.pl line 4643
	cpanel::cpanel::run_standard_mode() called at cpanel.pl line 931
	cpanel::cpanel::script("cpanel::cpanel", "./frontend/jupiter/lveversion/python-selector.html.tt") called at cpanel.pl line 324
"""