from django.urls import path

from todolist.goals import views

urlpatterns = [
    path('goal_category/create', views.GoalCategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', views.GoalCategoryListView.as_view(), name='category-list'),
    path('goal_category/<int:pk>', views.GoalCategoryView.as_view(), name='category-details'),
    # path("goal/create", views.GoalCreateView.as_view(), name='create-goal'),
    # path("goal/list", views.GoalListView.as_view(), name='goal-list'),
    # path("goal/<pk>", views.GoalView.as_view(), name='goal-details'),
    # path("goal_comment/create", views.GoalCommentCreateView.as_view(), name='create-goal-comment'),
    # path("goal_comment/list", views.GoalCommentListView.as_view(), name='goal-comment-list'),
    # path("goal_comment/<pk>", views.GoalCommentView.as_view(), name='goal-comment-details'),
    # path("board/", include("boards.urls")),
]
