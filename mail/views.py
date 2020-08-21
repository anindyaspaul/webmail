from django.shortcuts import render

# Create your views here.

class HomeView(View):
    template_name = 'base.html'
    
    def get(self, request):
        return render(request, self.template_name)
