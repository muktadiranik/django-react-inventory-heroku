from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
# Create your views here.
from .models import Category, Image, File


class Index(View):
    def get(self, request):
        categories = Category.objects.prefetch_related(
            "image_set").prefetch_related("file_set").all()

        return render(request, "upload/index.html", {
            "categories": categories,
        })

    # add new category
    def post(self, request):
        category_title = request.POST["title"]

        Category.objects.create(title=category_title)

        return redirect("upload-index")


# get images and files for specific category
class CategoryImageFile(View):
    def get(self, request, pk):
        categories = Category.objects.prefetch_related(
            "image_set").prefetch_related(
                "file_set").filter(pk=pk)

        return render(request, "upload/index.html", {
            "categories": categories,
        })


class UploadImage(View):
    def post(self, request):
        category_id = request.POST["category_id"]
        category = Category.objects.get(pk=category_id)
        images = request.FILES.getlist("images")

        image_list = [Image(category=category, image=image)
                      for image in images]

        Image.objects.bulk_create(image_list)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class UploadFile(View):
    def post(self, request):
        category_id = request.POST["category_id"]
        category = Category.objects.get(pk=category_id)
        files = request.FILES.getlist("files")

        file_list = [File(category=category, file=file)
                     for file in files]

        File.objects.bulk_create(file_list)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DeleteCategory(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()

        return redirect("upload-index")


class DeleteImage(View):
    def get(self, request, pk):
        image = Image.objects.get(pk=pk)
        image.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DeleteFile(View):
    def get(self, request, pk):
        file = File.objects.get(pk=pk)
        file.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
