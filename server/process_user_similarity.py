'''
 @author Rahul Raghavan
 This file is used to determine the similarity based on,
 factors like User Interests, User Course Views, User Assessments
'''
import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics.pairwise import pairwise_distances
from user import User

def readDataSources(file_path):
	'''
		Read datasource based on file path - csv files
	'''
	return pd.read_csv(file_path)


def initializeSimilarityMatrix(n_users, n_items, user_index, item_index, data_matrix):
	'''
		Initialize similarity matrix for n_users and n_items
	'''
	user_item_matrix = np.zeros((n_users, n_items))
	for line in data_matrix.itertuples():
	    user_item_matrix[line[user_index]-1, line[item_index]-1] = 1
	return user_item_matrix

def determineCosineSimilarity(user_item_matrix):
	'''
		Determine cosine similarity between users and return pairwise distance
		I have used memory based Collabrative filtering
	'''
	user_similarity = pairwise_distances(user_item_matrix, metric='cosine')
	return user_similarity;

def main(input_user_handle):
	'''
		Read from datasources, preprocess the data
		Calculate similarity metric
	'''
	input_user_handle = int(input_user_handle)
	course_tags = readDataSources("./course_tags.csv") 
	user_interests = readDataSources("./user_interests.csv") 
	user_assesments = readDataSources("./user_assessment_scores.csv") 
	user_course_views = readDataSources("./user_course_views.csv") 
	# Remove NULL Columns
	user_assesments=user_assesments.dropna(axis=1,how='all')
	user_interests=user_interests.dropna(axis=1,how='all')
	user_course_views=user_course_views.dropna(axis=1,how='all')
	course_tags=course_tags.dropna(axis=1,how='all')
	# Remove course based on criteria of watching greater than 5 minues
	user_course_views = user_course_views.drop(user_course_views[user_course_views.view_time_seconds < 300].index)
	# Convert categorical variables
	user_interests.interest_tag = pd.Categorical(user_interests.interest_tag)
	user_interests['code'] = user_interests.interest_tag.cat.codes
	n_users = max(user_interests.user_handle)
	n_items = max(user_interests.code)
	user_interests_matrix = initializeSimilarityMatrix(n_users,n_items,1,4, user_interests);
	user_interest_similarity = determineCosineSimilarity(user_interests_matrix);
	user_interest_similarity = 1-user_interest_similarity[input_user_handle]
	#print(user_interest_similarity)
	merged_course_views = pd.merge(user_course_views, course_tags, on='course_id')
	merged_course_views.course_tags = pd.Categorical(merged_course_views.course_tags)
	merged_course_views['code'] = merged_course_views.course_tags.cat.codes
	# Remove NULL and NA columns
	merged_course_views=merged_course_views.dropna(axis=1,how='all')
	n_users = max(merged_course_views.user_handle)
	n_items = max(merged_course_views.code)
	user_course_view_matrix = initializeSimilarityMatrix(n_users,n_items,1,8, merged_course_views);
	user_course_similarity = determineCosineSimilarity(user_course_view_matrix)
	user_course_similarity = 1-user_course_similarity[input_user_handle]
	user_assesments.assessment_tag = pd.Categorical(user_assesments.assessment_tag)
	user_assesments['code'] = user_assesments.assessment_tag.cat.codes
	n_users = max(user_assesments.user_handle)+1
	n_items = max(user_assesments.code)
	user_assesment_matrix = initializeSimilarityMatrix(n_users,n_items,1,5, user_assesments);
	user_assesment_similarity = determineCosineSimilarity(user_assesment_matrix)
	user_assesment_similarity = 1 - user_assesment_similarity[input_user_handle]

	'''
		Performed Weighted Aggregation, User interest and User Course being the most important and then user assesment
	'''
	user_agg_similarity  = user_interest_similarity + (0.5)*user_course_similarity +(0.2)* user_assesment_similarity
	idx = np.argsort(user_agg_similarity, axis=0);

	top_thirty_similar_users = idx[::-1][1:30];
	top_thirty_similarity_score = np.sort(user_agg_similarity);
	top_thirty_similarity_score = top_thirty_similarity_score[::-1][1:30]
	user = User();
	top_thirty_similar_users = np.array2string(top_thirty_similar_users, separator=',')
	top_thirty_similar_score = np.array2string(top_thirty_similarity_score, separator=',')
	# insert or update to db
	user = User()
	print(top_thirty_similarity_users)
	print(top_thirty_similarity_score)
	user.createNewUser(input_user_handle, top_thirty_similar_users, top_thirty_similar_score));





		
if __name__ == '__main__':
	input_user_handle = sys.argv[1];
	main(int(input_user_handle))
		

