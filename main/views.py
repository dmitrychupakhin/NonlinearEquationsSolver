from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse
from sympy import symbols, sympify, lambdify, diff
import math
import time
# Create your views here.


def dichotomy_method(f, a, b, step, epsilon):
    if f.subs(symbols('x'), a) * f.subs(symbols('x'), b) > 0:
        return None
    k = 1
    T0 = time.time()
    
    while (b - a) / 2 > epsilon:
        c = (a + b) / 2
        if abs(f.subs(symbols('x'), c)) < step:
            T1 = time.time()
            return c, (T1 - T0) * 1000, k
        elif f.subs(symbols('x'), a) * f.subs(symbols('x'), c) < 0:
            b = c
        else:
            a = c
        k += 1
            
    T1 = time.time()
    
    return (a + b) / 2, (T1 - T0) * 1000, k


def chord_method(f, a, b, step, epsilon):
    if f.subs(symbols('x'), a) * f.subs(symbols('x'), b) > 0:
        return None

    T0 = time.time()
    k = 1
    while (b - a) / 2 > epsilon:
        c = a - (b - a) * f.subs(symbols('x'), a) / (f.subs(symbols('x'), b) - f.subs(symbols('x'), a))
        if abs(f.subs(symbols('x'), c)) < step:
            T1 = time.time()
            return c, (T1 - T0) * 1000, k
        elif f.subs(symbols('x'), a) * f.subs(symbols('x'), c) < 0:
            b = c
        else:
            a = c
            
        k += 1
    T1 = time.time()
    return (a + b) / 2, (T1 - T0) * 1000, k

def newton_method(f, df, a, epsilon):
    T0 = time.time()
    k = 1
    while True:
        b = a - f.subs(symbols('x'), a) / df.subs(symbols('x'), a)
        if abs(b - a) < epsilon:
            break
        a = b
        k += 1
    T1 = time.time()
    return b, (T1 - T0) * 1000, k

def secant_method(f, a, b, epsilon):
    T0 = time.time()
    k = 0
    while True:
        c = b - f.subs(symbols('x'), b) * (b - a) / (f.subs(symbols('x'), b) - f.subs(symbols('x'), a))
        if abs(c - b) < epsilon:
            T1 = time.time()
            return b, (T1 - T0) * 1000, k
        a = b
        b = c
        k += 1

def gibrid_method(f, a, b,step, epsilon):
    t = (a + b) / 2
    k = 1
    T0 = time.time()
    while abs(f.subs(symbols('x'), t))> epsilon and min(abs(a - t), abs(b - t)) > step:
        if f.diff().subs(symbols('x'), t) == 0:
            if f.subs(symbols('x'), a) * f.subs(symbols('x'), t) < 0:
                b = t
            else:
                a = t
            t = a - f.subs(symbols('x'), a) * (b - a) / (f.subs(symbols('x'), b) - f.subs(symbols('x'), a))
        else:
            t_pred = t
            t = t_pred - f.subs(symbols('x'), t_pred) / f.diff().subs(symbols('x'), t_pred)
            if abs(f.subs(symbols('x'), t)) < abs(f.subs(symbols('x'), t_pred)):
                t = t
            else:
                t = 1 / 2 * (t_pred + t)
        k += 1

                
    T1 = time.time()
    return t, (T1 - T0) * 1000, k

def main(request):
    if request.method == 'POST':
        # Получение данных из формы
        x = symbols('x')
        try:
            function = sympify(request.POST.get('function'))
            start = float(request.POST.get('start'))
            end = float(request.POST.get('end'))
            step_size = float(request.POST.get('step_size'))
            accuracy = float(request.POST.get('accuracy'))   
            
            if function.subs(x, start) * function.subs(x, end) > 0:
                context = {
                    'error': 'Неверная функция',
                    'function': request.POST.get('function'),
                    'start': request.POST.get('start'),
                    'end': request.POST.get('end'),
                    'step_size': request.POST.get('step_size'),
                    'accuracy': request.POST.get('accuracy')
                }
                return render(request, 'main/home.html', context)
            
        except:
            context = {
                'error': 'Неправильные данные',
                'function': request.POST.get('function'),
                'start': request.POST.get('start'),
                'end': request.POST.get('end'),
                'step_size': request.POST.get('step_size'),
                'accuracy': request.POST.get('accuracy')
            }
            return render(request, 'main/home.html', context)
        
        context = {
                'function': request.POST.get('function'),
                'start': request.POST.get('start'),
                'end': request.POST.get('end'),
                'step_size': request.POST.get('step_size'),
                'accuracy': request.POST.get('accuracy')
        }
        
        result = [dichotomy_method(function, start, end, step_size, accuracy),
                  chord_method(function, start, end, step_size, accuracy),
                  newton_method(function, function.diff(), start, accuracy),
                  secant_method(function, start, end, accuracy),
                  gibrid_method(function, start, end, step_size, accuracy)]
        
        context['result'] = result
        return render(request, 'main/home.html', context)
    else:
        return render(request, 'main/home.html')