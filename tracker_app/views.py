from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import RecyclingActivity
from .forms import RecyclingActivityForm
import pandas as pd
import plotly.express as px
from django.db.models import Sum
from django.contrib.auth.models import User



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def home(request):
    if request.method == 'POST':
        form = RecyclingActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('home')
    else:
        form = RecyclingActivityForm()

    activities = RecyclingActivity.objects.filter(user=request.user).order_by('-date')[:5]
    return render(request, 'home.html', {'form': form, 'activities': activities})


@login_required
def statistics(request):
    activities = RecyclingActivity.objects.filter(user=request.user)
    df = pd.DataFrame(list(activities.values()))

    if not df.empty:
        # Calculate total recycled amount
        total_recycled = df[['plastic', 'paper', 'glass', 'metal']].sum().sum()

        # Sum up each material
        material_totals = df[['plastic', 'paper', 'glass', 'metal']].sum()

        # Create a new DataFrame for plotting
        df_totals = pd.DataFrame({
            'material': ['Plastic', 'Paper', 'Glass', 'Metal'],
            'amount': material_totals.values
        })

        # Create the pie chart
        fig = px.pie(df_totals, values='amount', names='material', title='Your Recycling Breakdown')
        chart = fig.to_html(full_html=False)
    else:
        total_recycled = 0
        chart = None

    return render(request, 'statistics.html', {'total_recycled': total_recycled, 'chart': chart})


@login_required
def leaderboard(request):
    top_users = User.objects.annotate(
        total_recycled=Sum('recyclingactivity__plastic') + Sum('recyclingactivity__paper') + Sum('recyclingactivity__glass') + Sum('recyclingactivity__metal')
    ).order_by('-total_recycled')[:10]

    return render(request, 'leaderboard.html', {'top_users': top_users})