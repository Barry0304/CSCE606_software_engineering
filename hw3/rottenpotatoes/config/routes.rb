# frozen_string_literal: true

Rottenpotatoes::Application.routes.draw do
  resources :movies
  # map '/' to be a redirect to '/movies'
  root to: redirect('/movies')
  match 'movies/:id/find_similar', to: 'movies#find_similar', as: 'similar_movies', via: :get
end
