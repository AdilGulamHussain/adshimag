
from django.conf.urls import url
from mag import views as mag_view


urlpatterns = [
    url(r'^$', mag_view.index, name='index'),
    url(r'^category/$', mag_view.all_categories, name="categories"),
    url(r'^article/(?P<a_id>[^.]+)$', mag_view.article_view, name='get_article'),
    url(r'^category/(?P<c_title>[-\w]+)$', mag_view.articles_in_category, name='articles_category'),
    url(r'^register/$', mag_view.register, name='register'),
    url(r'^login/$', mag_view.process_login, name='login'),
    url(r'^logout', mag_view.logout, name='logout'),
    url(r'^new_comment', mag_view.new_comment, name='new_comment'),
    url(r'^dashboard', mag_view.dash, name='dashboard'),
    url(r'^like', mag_view.like, name='liking'),
    url(r'^delComment', mag_view.delete_comment, name='del_comment'),
    url(r'^update', mag_view.update_details, name='update_details'),
]
