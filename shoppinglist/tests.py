from django.test import TestCase
from rest_framework.test import APIClient as Client
from django.urls import reverse
from rest_framework import status
from .models import CustomUser, List, Product, SharedList
from rest_framework_simplejwt.tokens import AccessToken

'''
    CRUD test for User (only creation), List, Product, and SharedList
'''

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="test@example.com", password="test")
        self.list = List.objects.create(user=self.user,
                                        name="Groceries",
                                        color="orange",
                                        total=0,
                                        checked=0,
                                        description="Buy some fish",
                                        complete=False)
        self.product = Product.objects.create(user=self.user, list=self.list, name="Apples", quantity=5)
        self.shared_list = SharedList.objects.create(user=self.user, list=self.list, list_name="Shared List", access_token="abc123")

    def test_custom_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(str(self.user), "test@example.com")
        self.assertEqual(self.user.password, "test")
        self.assertEqual(str(self.user.password), "test")

    def test_list_creation(self):
        list = List.objects.create(user=self.user, name="Groceries")
        self.assertEqual(list.name, "Groceries")
        self.assertEqual(list.user, self.user)

    def test_product_creation(self):
        list = List.objects.create(user=self.user, name="Groceries")
        product = Product.objects.create(
            user=self.user, list=list, name="Apples", quantity=5)
        self.assertEqual(product.name, "Apples")
        self.assertEqual(product.quantity, 5)
        self.assertEqual(product.list, list)

    def test_shared_list_creation(self):
        shared_list = SharedList.objects.create(user=self.user,
                                                list_name=self.list.name,
                                                access_token="abc123",
                                                list_id=self.list.pk)
        self.assertEqual(shared_list.list_name, self.list.name)
        self.assertEqual(shared_list.access_token, "abc123")
        self.assertEqual(shared_list.user, self.user)

    def test_list_update(self):
        updated_name = "Updated List Name"
        self.list.name = updated_name
        self.list.save()
        self.assertEqual(self.list.name, updated_name)

    def test_product_update(self):
        updated_quantity = 10
        self.product.quantity = updated_quantity
        self.product.save()
        self.assertEqual(self.product.quantity, updated_quantity)

    def test_shared_list_update(self):
        updated_token = "xyz456"
        self.shared_list.access_token = updated_token
        self.shared_list.save()
        self.assertEqual(self.shared_list.access_token, updated_token)

    def test_list_destruction(self):
        list_count_before = List.objects.count()
        self.list.delete()
        list_count_after = List.objects.count()
        self.assertEqual(list_count_before - 1, list_count_after)

    def test_product_destruction(self):
        product_count_before = Product.objects.count()
        self.product.delete()
        product_count_after = Product.objects.count()
        self.assertEqual(product_count_before - 1, product_count_after)

    def test_shared_list_destruction(self):
        shared_list_count_before = SharedList.objects.count()
        self.shared_list.delete()
        shared_list_count_after = SharedList.objects.count()
        self.assertEqual(shared_list_count_before - 1, shared_list_count_after)

    def test_list_listing(self):
        lists = List.objects.all()
        self.assertEqual(lists.count(), 1)
        self.assertEqual(lists[0].name, "Groceries")

    def test_product_listing(self):
        products = Product.objects.all()
        self.assertEqual(products.count(), 1)
        self.assertEqual(products[0].name, "Apples")

    def test_shared_list_listing(self):
        shared_lists = SharedList.objects.all()
        self.assertEqual(shared_lists.count(), 1)
        self.assertEqual(shared_lists[0].list_name, "Shared List")

class EndpointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email="test@example.com", password="testpass")
        self.list = List.objects.create(user=self.user,
                                        name="Groceries",
                                        color="orange",
                                        total=0,
                                        checked=0,
                                        description="Buy some fish",
                                        complete=False)
        self.product = Product.objects.create(name="Product 1", list=self.list, user=self.user)
        self.sharedList = SharedList.objects.create(access_token="abcddaaad", user=self.user, list=self.list)
        self.client.login(email="test@example.com", password="testpass")
        self.jwt_token = str(AccessToken.for_user(self.user))
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.jwt_token}'}


    #      user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")    
    # list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='shared_list', default="")
    # list_name = models.CharField(max_length=255, default="")
    # access_token = models.CharField(max_length=255, default="")

    '''
        ##########################################
        ## SharedList Endpoint Test Cases Start ##
        ##########################################
    '''    
    def test_sharedList_creation_endpoint(self):
        # Test POST request to create a shared list
        list = List.objects.create(user=self.user,
                                        name="Groceries",
                                        color="orange",
                                        description="Buy some fish",
                                        complete=False)
        list_data = {"list_name": list.name, "access_token": "abc", "user": self.user.pk, "list_id": list.pk}
        response = self.client.post(reverse("sharedList-create-list-destroy"), data=list_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sharedList_list_endpoint(self):
        # Test GET request to list all shared lists
        list1 = List.objects.create(user=self.user,
                                        name="Groceries",
                                        color="orange",
                                        description="Buy some fish",
                                        complete=False)
        list2 = List.objects.create(user=self.user,
                                        name="Gas",
                                        color="purple",
                                        description="Canadian Tire",
                                        complete=False)
        SharedList.objects.create(access_token="abc", user=self.user, list=list1)
        SharedList.objects.create(access_token="def", user=self.user, list=list2)
        response = self.client.get(reverse("sharedList-create-list-destroy"), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_sharedList_delete_endpoint(self):
        # Test a DELETE request to the shared list endpoint
        response = self.client.delete(reverse("sharedList-create-list-destroy"), data={"pk": self.sharedList.pk})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(SharedList.objects.filter(pk=self.sharedList.pk).exists())
    
    def test_sharedList_retrieve_endpoint(self):
        # Test a GET request to retrieve a single shared list
        list = List.objects.create(user=self.user,
                                        name="Gas",
                                        color="purple",
                                        description="Canadian Tire",
                                        complete=False)
        sharedList = SharedList.objects.create(access_token="abc", list=list, user=self.user, list_name=list.name)
        response = self.client.get(reverse("sharedList-retrieve", args=[sharedList.access_token]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''
        ########################################
        ## SharedList Endpoint Test Cases End ##
        ########################################
    ''' 

    '''
        ####################################
        ## List Endpoint Test Cases Start ##
        ####################################
    '''

    def test_list_creation_endpoint(self):
        # Test POST request to create a list
        list_data = {"name": "Apple", "color": "orange", "description": "buy some orange", "user": self.user.pk, "list": 100}
        response = self.client.post(reverse("list-list-create"), data=list_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_list_endpoint(self):
        # Test GET request to get all lists of the user
        List.objects.create(name="List 1", user=self.user)
        List.objects.create(name="List 2", user=self.user)
        response = self.client.get(reverse("list-list-create"), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_delete_endpoint(self):
        # Test a DELETE request to the product endpoint
        response = self.client.delete(reverse("list-retrieve-update-destroy", args=[self.list.pk]))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(List.objects.filter(pk=self.list.pk).exists())

    def test_list_update_endpoint(self):
        # Test a PUT request to the list endpoint
        updated_data = {"name": "Walmart", "description": "Shopping list to walmart"}
        response = self.client.put(reverse("list-retrieve-update-destroy", args=[self.list.pk]), data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.list.refresh_from_db()
        self.assertEqual(self.list.name, "Walmart")
        self.assertEqual(self.list.description, "Shopping list to walmart")
    
    def test_list_retrieve_endpoint(self):
        # Test a GET request to retrieve a single list
        list = List.objects.create(name="Buy some Lego", description="Yorkdale", user=self.user)
        response = self.client.get(reverse("list-retrieve-update-destroy", args=[list.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("Buy some Lego", response.data["name"])
        self.assertEqual("Yorkdale", response.data["description"])

    '''
        ##################################
        ## List Endpoint Test Cases End ##
        ##################################
    '''

    '''
        #######################################
        ## Product Endpoint Test Cases Start ##
        #######################################
    '''

    def test_product_creation_endpoint(self):
        # Test POST request to create a product
        product_data = {"name": "Apple", "quantity": 5, "note": "buy two dozens", "list": self.list.pk, "user": self.user.pk}
        response = self.client.post(reverse("product-list-create"), data=product_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_product_list_endpoint(self):
        # Test GET request to get all products
        Product.objects.create(name="Product 1", list=self.list, user=self.user)
        Product.objects.create(name="Product 2", list=self.list, user=self.user)
        response = self.client.get(reverse("product-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_product_delete_endpoint(self):
        # Test a DELETE request to the product endpoint
        response = self.client.delete(reverse("product-destroy-retrieve-update", args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_update_endpoint(self):
        # Test a PUT request to the product endpoint
        updated_data = {"name": "Walmart", "note": "salmon"}
        response = self.client.put(reverse("product-destroy-retrieve-update", args=[self.product.pk]), data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Walmart")
        self.assertEqual(self.product.note, "salmon")
    
    def test_product_retrieve_endpoint(self):
        # Test a GET request to retrieve a single product
        product = Product.objects.create(name="Ginger", list=self.list, user=self.user)
        response = self.client.get(reverse("product-destroy-retrieve-update", args=[product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("Ginger", response.data["name"])

    '''
        #####################################
        ## Product Endpoint Test Cases End ##
        #####################################
    '''

    '''
        ####################################
        ## User Endpoint Test Cases Start ##
        ####################################
    '''

    def test_user_creation_endpoint(self):
        response = self.client.post(reverse("user-create"), {"email": "testCreate@example.com", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    '''
        ##################################
        ## User Endpoint Test Cases End ##
        ##################################
    '''

# class EndpointTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(email="test@example.com", password="testpass")
#         self.jwt_token = str(AccessToken.for_user(self.user))

#     def test_product_endpoints(self):
#         headers = {'HTTP_AUTHORIZATION': f'Bearer {self.jwt_token}'}

#         # Test POST request to create a product
#         product_data = {"name": "Apple", "quantity": 5}
#         response = self.client.post(reverse("product-list"), data=product_data, **headers)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Test PUT request to update a product
#         updated_product_data = {"name": "Updated Apple", "quantity": 10}
#         response = self.client.put(reverse("product-detail", args=[1]), data=updated_product_data, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # ...
