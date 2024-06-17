from django.shortcuts import render, redirect
from .models import Food, Consume


def index(request):
    
    food = Food.objects.all()
    consumed_food_by_user = Consume.objects.filter(user=request.user)

    if request.method == "POST":
        food_consumed = request.POST.get("food_consumed")
        print(food_consumed)
        food_object = Food.objects.get(pk=food_consumed)

        user = request.user

        consume = Consume(user=user, food_consumed=food_object)
        consume.save()

    context = {"foods": food,
               "consumed_foods": consumed_food_by_user}
    return render(request, "myapp/index.html", context)

def delete_item(request,id):
    selected_item = Consume.objects.get(id=id)
    selected_item.delete()
    return redirect('/')