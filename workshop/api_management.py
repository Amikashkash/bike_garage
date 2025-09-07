from rest_framework import generics, status, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import RepairCategory, RepairSubCategory
from .serializers import RepairCategorySerializer, RepairSubCategorySerializer
from .permissions import manager_required


class IsManagerPermission(permissions.BasePermission):
    """Permission class to check if user is a manager"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'manager'


@method_decorator(login_required, name='dispatch')
class CategoryManagementListView(generics.ListCreateAPIView):
    """List and create categories for managers"""
    serializer_class = RepairCategorySerializer
    permission_classes = [IsManagerPermission]
    queryset = RepairCategory.objects.all()

    def get_queryset(self):
        return RepairCategory.objects.prefetch_related('subcategories').all()

    def perform_create(self, serializer):
        serializer.save()


@method_decorator(login_required, name='dispatch')
class CategoryManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a category for managers"""
    serializer_class = RepairCategorySerializer
    permission_classes = [IsManagerPermission]
    queryset = RepairCategory.objects.all()

    def perform_destroy(self, instance):
        # Check if category has repairs associated with it via subcategories
        repair_count = sum(
            subcat.repair_jobs.count() 
            for subcat in instance.subcategories.all()
        )
        
        if repair_count > 0:
            raise serializers.ValidationError(
                f"Cannot delete category with {repair_count} associated repairs"
            )
        
        instance.delete()


@method_decorator(login_required, name='dispatch')
class SubcategoryManagementListView(generics.ListCreateAPIView):
    """List and create subcategories for managers"""
    serializer_class = RepairSubCategorySerializer
    permission_classes = [IsManagerPermission]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return RepairSubCategory.objects.filter(category_id=category_id)
        return RepairSubCategory.objects.all()

    def perform_create(self, serializer):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(RepairCategory, id=category_id)
            serializer.save(category=category)
        else:
            serializer.save()


@method_decorator(login_required, name='dispatch')
class SubcategoryManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a subcategory for managers"""
    serializer_class = RepairSubCategorySerializer
    permission_classes = [IsManagerPermission]
    queryset = RepairSubCategory.objects.all()

    def perform_destroy(self, instance):
        # Check if subcategory has repairs associated with it
        if instance.repair_jobs.exists():
            raise serializers.ValidationError(
                f"Cannot delete subcategory with {instance.repair_jobs.count()} associated repairs"
            )
        
        instance.delete()


@api_view(['POST'])
@login_required
@permission_classes([IsManagerPermission])
def batch_create_subcategories(request):
    """Create multiple subcategories for a category at once"""
    category_id = request.data.get('category_id')
    subcategories = request.data.get('subcategories', [])
    
    if not category_id:
        return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not subcategories:
        return Response({'error': 'Subcategories list is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = get_object_or_404(RepairCategory, id=category_id)
        created_subcategories = []
        
        with transaction.atomic():
            for subcategory_data in subcategories:
                name = subcategory_data.get('name', '').strip()
                if name:
                    # Check if subcategory already exists for this category
                    existing = RepairSubCategory.objects.filter(
                        category=category, 
                        name__iexact=name
                    ).first()
                    
                    if not existing:
                        subcategory = RepairSubCategory.objects.create(
                            category=category,
                            name=name
                        )
                        created_subcategories.append({
                            'id': subcategory.id,
                            'name': subcategory.name,
                            'category_id': category.id,
                            'category_name': category.name
                        })
        
        return Response({
            'message': f'{len(created_subcategories)} subcategories created successfully',
            'created_subcategories': created_subcategories,
            'category': {
                'id': category.id,
                'name': category.name
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
@permission_classes([IsManagerPermission])
def category_stats(request):
    """Get category statistics for the management dashboard"""
    categories_with_stats = []
    
    for category in RepairCategory.objects.prefetch_related('subcategories__repair_jobs'):
        subcategory_count = category.subcategories.count()
        total_repairs = sum(
            subcat.repair_jobs.count() 
            for subcat in category.subcategories.all()
        )
        
        categories_with_stats.append({
            'id': category.id,
            'name': category.name,
            'subcategory_count': subcategory_count,
            'total_repairs': total_repairs,
            'has_subcategories': subcategory_count > 0,
            'subcategories': [
                {
                    'id': subcat.id,
                    'name': subcat.name,
                    'repair_count': subcat.repair_jobs.count()
                }
                for subcat in category.subcategories.all()
            ]
        })
    
    return Response({
        'categories': categories_with_stats,
        'total_categories': len(categories_with_stats),
        'total_subcategories': sum(cat['subcategory_count'] for cat in categories_with_stats),
        'total_repairs': sum(cat['total_repairs'] for cat in categories_with_stats)
    })