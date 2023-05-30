from django import forms
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, View, DetailView
from django.utils import timezone
from datetime import timedelta
from newspaper.models import Post, Category, Tag, Newsletter, TimeStampModel
from newspaper.forms import CommentForm, ContactForm, NewsletterForm
from django.contrib import messages


class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(status="active", published_at__isnull=False)
            .order_by("-views_count")
            .first()
        )

        return context

        context["featured_posts"] = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[1:4]

        one_week_ago = timezone.now() - timedelta(days=7)

        context["weekly_top_posts"] = Post.objects.filter(
            status="active",
            published_at__gte=one_week_ago,
        ).order_by("-published_at", "-views_count")[:7]

        return context


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class PostListView(ListView):
    model = Post
    template_name = "aznews/main/list/list.html"
    paginate_by = 2
    queryset = Post.objects.filter(
        status="active",
        published_at__isnull=False,
    ).order_by("-published_at")
    context_object_name = "posts"


class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/main/list/list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            status="active",
            published_at__isnull=False,
            category=self.kwargs["category_id"],
        )
        return query


class PostByTagView(ListView):
    model = Post
    template_name = "aznews/main/list/list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            status="active",
            published_at__isnull=False,
            tag=self.kwargs["tag_id"],
        )
        return query


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/main/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            status="active",
            published_at__isnull=False,
        )
        return query

        def get_context_data(self,*args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            obj = self.get_object()  #get current post view
            obj.views_count += 1
            obj.save()

            context["previous_post"] = (
                Post.objects.filter(
                    status="active", published_at__isnull=False, id__lt=obj.id
                )
                .order_by("-id")
                .first()
            )

            context["next_post"] = (
                Post.objects.filter(
                    status="active", published_at__isnull=False, id__gt=obj.id
                )
                .order_by("id")
                .first()
            )
            return context


class ContactView(View):
    template_name = "aznews/contact.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "query submitted.")
            return redirect("contact")
        else:
            messages.error(request, "Cannot submit your query.")
            return render(
                request,
                self.template_name,
                {"form": form},
            )


class NewsletterView(View): 

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {"success": True, "message": "Subscribed successfully."},
                    status=201,
                )
            else:
                return JsonResponse(
                    {"success": False, "message": "Email is not valid."},
                    status=400,
                )
        return JsonResponse({"success": False, "message": "cannot process"}, status=400)

class CommentView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST['post']
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)
        
        else:
            post = Post.objects.get(pk=post_id)
            return render(
                request,
                "aznews/main/detail/detail.html",
                {"post": post, "form": form},
            )