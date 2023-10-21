from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from mychart.settings import BASE_DIR
from mysite.forms import TextFileUploadForm
from mysite.models import Population
import jieba, json, io, base64, urllib.parse
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from translate import Translator

def index(request):
    return render(request, "index.html", locals())

def cut(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":
            d = json.load(request)
            rawdata = d.get('payload')
            cutted = [w for w in jieba.cut(rawdata)]
            data = "/".join(cutted)
            return JsonResponse({"data":data}, status=200)
        else:
            pass
    return render(request, "cut.html", locals())

def wordcloud(request):
    if request.method == "POST":
        textdata = request.FILES['file'].read()
        data = [w for w in jieba.cut(textdata)]
        words = ",".join(data)
        mask = np.array(Image.open('cloud.jpg'))
        wordcloud = WordCloud(background_color = "White",
                              width=1000, height=860, margin=2,
                              font_path= 'SimHei.ttf',
                              mask=mask).generate(words)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        image = io.BytesIO()
        plt.savefig(image, format="png")
        image.seek(0)
        img_data = base64.b64encode(image.read()).decode("utf-8")
        form = TextFileUploadForm()
        return render(request, "wordcloud.html", locals())
    else:
        form = TextFileUploadForm()
    return render(request, "wordcloud.html", locals())

def heartcurve(request):
    chart_name = "笛卡爾心形線"
    th = np.linspace(0, 2*np.pi, 100)
    x = (1 - np.cos(th)) * np.sin(th)
    y = (1 - np.cos(th)) * np.cos(th)
    plt.figure()
    plt.plot(x, y)
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def heartcurve_polar(request):
    chart_name = "笛卡爾心形線(Polar)"
    th = np.linspace(0, 2*np.pi, 100)
    r = 2 * (1 - np.sin(th))
    plt.figure()
    gr = plt.subplot(111, polar=True)
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def mat_bar(request):
    chart_name = "長條圖"
    data = Population.objects.annotate(t=F('male')+F('female')).all().order_by('-t')
    population = [d.male for d in data]
    trans = Translator(to_lang="en")
    names = [trans.translate(d.name) for d in data]
    print(names)
    plt.figure()
    plt.barh(range(len(population)), population, tick_label=names)
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def mat_line(request):
    chart_name = "折線圖"
    return render(request, "mat-image.html", locals())

def mat_scatter(request):
    chart_name = "散佈圖"
    return render(request, "mat-image.html", locals())

def mat_3d(request):
    chart_name = "3D立體圖"
    return render(request, "mat-image.html", locals())