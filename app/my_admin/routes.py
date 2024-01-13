from flask_admin import AdminIndexView, expose

class MyAdminIndexView(AdminIndexView):
  @expose("/")
  def index(self):
    return self.render("admin/my_admin_home_page.html")