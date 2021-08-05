import re
import pickle
import uuid
from abc import ABC

from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import request
import surprise
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from users.models import Profile
from . import models
from .models import Product, Review
from sklearn.feature_extraction.text import TfidfVectorizer


class ProductListView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'
    ordering = ['-date_added']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = [
    ('All Products','All Products'),
    ('Movies & TV', 'Movies & TV'),
    ('Sports & Outdoors', 'Sports & Outdoors'),
    ('Fashion', 'Fashion'),
    ('Amazon Home', 'Amazon Home'),
    ('Health & Personal Care', 'Health & Personal Care'),
    ('Books', 'Books'),
    ('Toys & Games', 'Toys & Games'),
    ('Baby', 'Baby'),
    ('Office Products', 'Office Products'),
    ('All Beauty', 'All Beauty'),
    ('Arts, Crafts & Sewing', 'Arts, Crafts & Sewing'),
    ('Digital Music', 'Digital Music'),
    ('Home Audio & Theater', 'Home Audio & Theater'),
    ('Video Games', 'Video Games'),
    ('Tools & Home Improvement', 'Tools & Home Improvement'),
    ('All Electronics', 'All Electronics'),
    ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
    ('AMAZON FASHION', 'AMAZON FASHION'),
    ('Camera & Photo', 'Camera & Photo'),
    ('Industrial & Scientific', 'Industrial & Scientific'),
    ('Musical Instruments', 'Musical Instruments'),
    ('Automotive', 'Automotive'),
    ('Computers', 'Computers'),
    ('Grocery', 'Grocery'),
    ('Portable Audio & Accessories', 'Portable Audio & Accessories'),
    ('Software', 'Software'),
    ('Car Electronics', 'Car Electronics'),
    ('Pet Supplies', 'Pet Supplies'),
    ('Appliances', 'Appliances'),
    ('Collectible Coins', 'Collectible Coins'),
    ('Entertainment', 'Entertainment'),
    ('Luxury Beauty', 'Luxury Beauty'),
    ('GPS & Navigation', 'GPS & Navigation'),
    ('Amazon Devices', 'Amazon Devices')
]
        print(context['categories'])
        if self.request.user.is_authenticated:
            with open("django_modelSVD.pkl", 'rb') as file:
                modelReload = pickle.load(file)
                cfdf = pd.DataFrame(Review.objects.all().values('asin', 'reviewerID', 'overall'))
                cfdf['Estimate_Score'] = cfdf['asin'].apply(
                    lambda x: modelReload.predict(self.request.user.profile.id, x).est)
                context['cfmlreccomend'] = Product.objects.filter(
                    pk__in=cfdf.sort_values(by=['Estimate_Score'], ascending=False).head(10).index.tolist())
                context['carousel'] = Product.objects.filter(
                    pk__in=cfdf.sort_values(by=['Estimate_Score'], ascending=False).head(100).index.tolist())
                print(context['cfmlreccomend'])
                print(cfdf)
                print(self.request.user.profile.id)
        else:
            dfearlyrecc = pd.DataFrame(list(Review.objects.all().values('asin', 'reviewerID', 'overall')))
            earlyrecclist = dfearlyrecc.groupby('asin')['overall'].count().sort_values(ascending=False).head(10)
            context['earlyreccomend'] = Product.objects.filter(pk__in=earlyrecclist.index.tolist())
            context['carousel'] = Product.objects.filter(imageUrl__isnull=False)[0:100]
        return context


class UserReviewListView(ListView):
    model = Review
    template_name = 'store/user_reviews.html'
    context_object_name = 'review'
    ordering = ['-date_added']
    paginate_by = 10

    def get_queryset(self):
        pass


class ProductSearchView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'all_search_results'
    paginate_by = 10

    def get_queryset(self):
        result = super(ProductSearchView, self).get_queryset()
        query = self.request.GET.get('search')
        boxes = self.request.GET.get('category')
        print(boxes)
        if boxes == 'All Products':
            if query:
                postresult = Product.objects.filter(title__contains=query)
                result = postresult
            else:
                result = None
        else:
            if query == '':
                postresult = Product.objects.filter(main_cat__contains=boxes)
                result = postresult
            else:
                if query:
                    postresult = Product.objects.filter(main_cat__contains=boxes).filter(title__contains=query)
                    result = postresult
                else:
                    result = None
        return result


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['review'] = Review.objects.filter(asin=self.object.pk)
        context['also_view'] = Product.objects.filter(
            asin__in=self.object.also_view[1:-1].replace(" ", "").replace("'", "").split(","))
        context['also_buy'] = Product.objects.filter(
            asin__in=self.object.also_buy[1:-1].replace(" ", "").replace("'", "").split(","))
        # start vectorizer
        tfidf = TfidfVectorizer(stop_words='english')
        # make dataframe
        # search reviews and use as key to be used to search
        if Review.objects.filter(reviewerID=self.request.user).count() > 0:
            print("User has at least 1 review")
            # get the related reviews for the user
            usersreviews = Review.objects.filter(reviewerID=self.request.user).order_by('-overall')
            # get the related products
            userreviewrelatedproducts = Product.objects.filter(pk__in=usersreviews.values_list('asin_id', flat=True))
            qs = Product.objects.all()[abs(self.object.id - 40000):self.object.id + 40000]
            qs |= Product.objects.filter(id=self.object.id)
            qs |= Product.objects.filter(title=userreviewrelatedproducts.first().title)
            cbfdf = pd.DataFrame(
                qs.values('asin', 'title', 'description'))
            cbfdf.drop_duplicates(inplace=True)
            cbfdf.fillna(value='', inplace=True)
            # apply to the dataframe to remove extraneous words
            tfidf_matrix = tfidf.fit_transform(cbfdf['title'])
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
            indices = pd.Series(cbfdf.index, index=cbfdf['title']).drop_duplicates()
            idx = indices[userreviewrelatedproducts.first().title]
        else:
            print("User has no reviews")
            qs = Product.objects.all()[abs(self.object.id - 20000):self.object.id + 20000]
            qs |= Product.objects.filter(id=self.object.id)
            cbfdf = pd.DataFrame(
                qs.values('asin', 'title', 'description'))
            cbfdf.drop_duplicates(inplace=True)
            cbfdf.fillna(value='', inplace=True)
            # apply to the dataframe to remove extraneous words
            tfidf_matrix = tfidf.fit_transform(cbfdf['title'])
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
            indices = pd.Series(cbfdf.index, index=cbfdf['title']).drop_duplicates()
            idx = indices[self.object.title]
        # Get the pairwsie similarity scores of all product with that product
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort the products based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get the scores of the 10 most similar products
        sim_scores = sim_scores[1:11]
        # Get the product indices
        product_indices = [i[0] for i in sim_scores]
        # Return the top 10 most similar product
        context['cbfproducts'] = Product.objects.filter(pk__in=cbfdf['title'].iloc[product_indices].index.tolist())
        return context


class ReviewDetailView(DetailView):
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ReviewDetailView, self).get_context_data(**kwargs)
        context['rproduct'] = Product.objects.filter(asin=self.object.asin)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['reviewText', 'summary', 'overall', 'reviewerName']

    def form_valid(self, form):
        form.instance.reviewerID = self.request.user
        form.instance.asin = Product.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['reviewText', 'summary', 'overall', 'reviewerName']

    def test_func(self):
        review = self.get_object()
        print(self.request.user)
        print(review.reviewerID)
        if self.request.user == review.reviewerID:
            return True
        return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.reviewerID = self.request.user
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.reviewerID:
            return True
        return False


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'price', 'imageUrl', 'brand', 'description', 'details', 'category', 'main_cat', 'date_added']

    def form_valid(self, form):
        asin = uuid.uuid4()
        return super().form_valid(form)


def about(request):
    return render(request, 'store/about.html', {'title': 'About'})

