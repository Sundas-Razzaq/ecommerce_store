from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from django.urls import reverse

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile update
        profile.full_name = request.POST.get('full_name', '')
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address_line1 = request.POST.get('address_line1', '')
        profile.address_line2 = request.POST.get('address_line2', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', '')
        
        if 'picture' in request.FILES:
            if profile.picture:
                profile.picture.delete()
            profile.picture = request.FILES['picture']
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('core:home')
    
    return render(request, 'profiles/profile.html', {
        'profile': profile,
        'active_tab': 'profile'
    })

@login_required
def become_seller(request):
    profile = request.user.profile

    if request.user.is_superuser:
        messages.warning(request, "Admin cannot become a seller.")
        return redirect('profile')  # or wherever you want

    if profile.role == 'seller':
        messages.info(request, "You are already a seller.")
        return redirect('seller:become_seller')  

    profile.role = 'seller'
    profile.save()
    messages.success(request, "You are now a seller!")

    return redirect('seller:become_seller')  
