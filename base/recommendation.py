import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from base.models import Book
from django.contrib.auth.models import User
from base.models import Rating, Book, My_Book

class MatrixFactorization(nn.Module):
    def __init__(self, num_users,num_items,embedding_size=100):
        super(MatrixFactorization, self).__init__()
        self.user_embeddings = nn.Embedding(num_users, embedding_size, sparse=True)
        self.item_embeddings = nn.Embedding(num_items, embedding_size, sparse=True)
        #################################################
        self.user_embeddings.weight.data.uniform_(0, 0.05)
        self.item_embeddings.weight.data.uniform_(0, 0.05)
        
        # Model for Ui*Vj(Vector for users and vector for items)
    def forward(self, u, v):
        user_embedding = self.user_embeddings(u)
        item_embedding = self.item_embeddings(v)
        return (user_embedding * item_embedding).sum(1)
    
def predict(sample_user, sample_item):
    sample_user_id = torch.tensor([sample_user])
    predictions = []
    
    with torch.no_grad():
        for i in sample_item:
            # sample_item_id = torch.tensor([i])
            prediction = model(sample_user_id, i)
            predictions.append(prediction.item())
        # print(f'Predicted Rating: {predictions}')
    return torch.tensor(predictions)
    
model = MatrixFactorization(num_users=3705, num_items=70034, embedding_size=100)
model.load_state_dict(torch.load("base\matrix_factorization_model.pth"))
model.eval()


ratings = My_Book.objects.all()
books = Book.objects.all()
# Extract unique user and book IDs

user_ids = list(set(rating.user.pk for rating in ratings))
book_ids = list(set(book.pk for book in books))

# Create an empty user-item matrix filled with zeros
user_item_matrix = np.zeros((len(user_ids), len(book_ids)))

# Fill in the matrix with the ratings
for rating in ratings:
    user_index = user_ids.index(rating.user.pk)
    book_index = book_ids.index(rating.book.pk)
    user_item_matrix[user_index, book_index] = rating.rating.rating

# Display the user-item matrix
print("User-Item Matrix:")
print(user_item_matrix)

def get_recommendations(user_id, model, user_item_matrix, num_recommendations=3):

    sample_user_id = user_id - 1
    # sample_item_id = torch.tensor([book])

    user_row = user_item_matrix[0, :]
    unrated_books = torch.tensor([book_id for book_id, rating in enumerate(user_row) if rating == 0])
    
    with torch.no_grad():
        predicted_ratings = predict(user_id, unrated_books)
        sorted_books = [book_id for _, book_id in sorted(zip(predicted_ratings, unrated_books.numpy()), reverse=True)]

        # recommended_books_indices = torch.argsort(predicted_ratings, descending=True)[:5]
        
    recommended_books_indices = sorted_books[:num_recommendations]
    recommended_books = []
    for i in recommended_books_indices:
        a = Book.objects.get(id=i)
        recommended_books.append(a)

    # print(recommended_books_indices)
    return recommended_books_indices

# predict(3,2)
# get_recommendations(1, model, user_item_matrix, num_recommendations=5)





