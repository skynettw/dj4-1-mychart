from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from mychart.settings import BASE_DIR
from mysite.forms import TextFileUploadForm
from mysite.models import Population
import jieba, json, io, base64, urllib.parse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from wordcloud import WordCloud
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
from PIL import Image
import pandas as pd

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
    data = Population.objects.annotate(t=F('male')+F('female')).all().order_by('t')
    population = [d.male for d in data]
    names = [d.name for d in data]
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure()
    plt.title("112年各縣市人口排行")
    plt.xlim((0, 4000000))
    plt.xlabel("百萬人")
    plt.grid()
    plt.barh(range(len(population)), population, tick_label=names)
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def mat_line(request):
    chart_name = "折線圖"
    df = pd.read_csv('tokyo.csv')
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure()
    plt.plot(df['high'], label="高溫")
    plt.plot(df['low'], label="低溫")
    plt.bar(range(0, 12), height=df['rain'], label="降雨天數")
    plt.ylim((0, 40))
    plt.title("東京月平均氣溫及降雨天數")
    plt.xlabel("月份")
    plt.xticks(range(0, 12), range(1, 13))
    plt.ylabel("攝氏度或天數")
    plt.legend()
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def mat_scatter(request):
    chart_name = "散佈圖"
    df = pd.read_csv('tokyo.csv')
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure()
    plt.scatter(df['rain'], df['high'])
    plt.xlim((0, 15))
    plt.ylim((0, 40))
    plt.title("東京月溫度與降雨天數關係圖")
    plt.xlabel("降雨天數")
    plt.ylabel("月均高溫")
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def mat_3d(request):
    chart_name = "3D立體圖"
    matplotlib.rc('font', family='Times New Roman')
    fig = plt.figure()
    axis = fig.add_subplot(projection = '3d')
    x = np.arange(-2.0, 2.0, 0.1)
    y = np.arange(-2.0, 2.0, 0.1)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2
    surface = axis.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='twilight')
    fig.colorbar(surface, shrink=1.0, aspect=20)
    fig.gca().set_xlabel('x')
    fig.gca().set_ylabel('y')
    fig.gca().set_title(r'z = x$^{2}$ - y$^{2}$')
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img_data = base64.b64encode(image.read()).decode("utf-8")
    return render(request, "mat-image.html", locals())

def getdata(request):
    data = dict()
    df = pd.read_csv("tokyo.csv")
    data['label'] = df['month'].values.tolist()
    data['value'] = df['high'].values.tolist()
    return JsonResponse(json.dumps(data), safe=False)

def chartjs_bar(request):
    return render(request, "chartjs-bar.html", locals())

def chartjs_line(request):
    return render(request, "chartjs-line.html", locals())

def plotly_curve(request):
    chart_name = "Plotly 函數圖形"
    x = np.linspace(0, 2*np.pi, 360)
    y1 = np.sin(x)
    y2 = np.cos(x)
    plot_div = plot([go.Scatter(x=x, y=y1,
		mode='lines', name='SIN', text="正弦波形圖",
		opacity=0.8, marker_color='green'),
		go.Scatter(x=x, y=y2,
		mode='lines', name='COS', text="餘弦波形圖",
		opacity=0.8, marker_color='blue')],
		output_type='div')
    return render(request, "plotly-chart.html", locals())
    
def plotly_bar(request):
    chart_name = "Plotly直條圖（台灣各縣市人口統計排行）"
    data = Population.objects.annotate(t=F('male')+F('female')).all().order_by('-t')
    population = [d.male for d in data]
    names = [d.name for d in data]
    df = pd.read_csv("tokyo.csv")
    data = [go.Bar(
        x = names,
        y = population
    )]
    plot_div = plot(data, output_type='div')
    return render(request, "plotly-chart.html", locals())

def plotly_line(request):
    chart_name = "Plotly折線圖（東京月平均降雨天數）"
    df = pd.read_csv("tokyo.csv")
    
    plot_div = plot([go.Scatter(y=df['rain'].values.tolist(),
		mode='lines', name='Rainfall days', text="降雨天數",
		opacity=0.8, marker_color='green')],
		output_type='div')
    return render(request, "plotly-chart.html", locals())

def plotly_3d(request):
    chart_name = "Plotly折線圖（立體函數圖）"
    z = np.linspace(0, 10, 100)
    x = np.cos(z)
    y = np.sin(z)
    trace = go.Scatter3d(
    x = x, y = y, z = z,mode = 'markers', marker = dict(
      size = 3,
      color = x, 
      colorscale = 'rainbow'
      )
    )
    layout = go.Layout(title = '3D 函數圖形')
    data = go.Figure(data = [trace], layout = layout)
    plot_div = plot(data, output_type='div')
    return render(request, "plotly-chart.html", locals())