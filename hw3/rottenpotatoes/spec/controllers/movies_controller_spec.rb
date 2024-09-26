# frozen_string_literal: true

require 'rails_helper'

RSpec.describe MoviesController, type: :controller do
  before do
    Movie.destroy_all

    Movie.create(title: 'Big Hero 6', rating: 'PG', release_date: '2014-11-07', director: 'Don Hall, Chris Williams')
    Movie.create(title: 'Inception', rating: 'PG-13', release_date: '2010-07-16', director: 'Christopher Nolan')
    Movie.create(title: 'Interstellar', rating: 'PG-13', release_date: '2014-11-07', director: 'Christopher Nolan')
    Movie.create(title: 'Alien', rating: 'R', release_date: '1979-05-25', director: 'Ridley Scott')
    Movie.create(title: 'Blade Runner', rating: 'R', release_date: '1982-06-25', director: 'Ridley Scott')
  end

  def get_find_similar(movie)
    get :find_similar, params: { id: movie.id }
  end

  describe 'when trying to find movies by the same director' do
    let!(:movie) { Movie.create(title: 'Inception', director: 'Christopher Nolan') }
    let!(:movie2) { Movie.create(title: 'Interstellar', director: 'Christopher Nolan') }

    it 'returns a valid collection when a valid director is present' do
      get_find_similar(movie)
      expect(assigns(:similar_movies)).to include(movie2)
    end

    it 'redirects to index when no director is present' do
      movie_no_director = Movie.create(title: 'Unknown Movie', director: nil)
      get_find_similar(movie_no_director)
      expect(response).to redirect_to(movies_path)
    end

    it 'sets the flash message when no director is present' do
      movie_no_director = Movie.create(title: 'Unknown Movie', director: nil)
      get_find_similar(movie_no_director)
      expect(flash[:notice]).to match(/has no director info/)
    end
  end

  describe 'creates' do
    let(:movie_params) do
      { movie: { title: 'Threenagers', director: 'The Prof.s Ritchey', rating: 'G', release_date: '2015-01-20' } }
    end

    it 'redirects to the movies list after creation' do
      get :create, params: movie_params
      expect(response).to redirect_to movies_path
    end

    it 'sets a flash notice after movie creation' do
      get :create, params: movie_params
      expect(flash[:notice]).to match(/Threenagers was successfully created./)
      Movie.find_by(title: 'Threenagers').destroy
    end
  end

  describe 'updates' do
    let!(:movie) do
      Movie.create(title: 'Attack of the Munchkins', director: 'Sofia Grace', rating: 'PG', release_date: '2024-08-19')
    end

    after { movie.destroy }

    it 'redirects to the movie details page after update' do
      get :update, params: { id: movie.id,
                             movie: {
                               description: 'A whimsical film where a town is overrun.'
                             } }
      expect(response).to redirect_to movie_path(movie)
    end

    it 'sets a flash notice after movie update' do
      get :update, params: { id: movie.id, movie: { description: 'A whimsical and adventurous film...' } }
      expect(flash[:notice]).to match(/Attack of the Munchkins was successfully updated./)
    end

    it 'updates the movie record' do
      new_director = 'Akira Kurosawa'
      get :update, params: { id: movie.id, movie: { director: new_director } }
      expect(assigns(:movie).director).to eq(new_director)
    end
  end

  describe 'GET find_similar' do
    let!(:movie) { Movie.create(title: 'Alien', director: 'Ridley Scott') }
    let!(:movie2) { Movie.create(title: 'Blade Runner', director: 'Ridley Scott') }

    it 'finds movies by the same director' do
      get_find_similar(movie)
      expect(assigns(:similar_movies)).to include(movie2)
    end

    it 'redirects to index when no director is present' do
      movie_no_director = Movie.create(title: 'Alien', director: nil)
      get_find_similar(movie_no_director)
      expect(response).to redirect_to(movies_path)
    end

    it 'sets the flash notice when no director is present' do
      movie_no_director = Movie.create(title: 'Alien', director: nil)
      get_find_similar(movie_no_director)
      expect(flash[:notice]).to match(/has no director info/)
    end
  end

  describe 'DELETE destroy' do
    let!(:movie) do
      Movie.create(title: 'Test Movie', director: 'Test Director', rating: 'PG', release_date: '2024-01-01')
    end

    it 'deletes the movie from the database' do
      expect { delete :destroy, params: { id: movie.id } }.to change(Movie, :count).by(-1)
    end

    it 'redirects to the movies index after deletion' do
      delete :destroy, params: { id: movie.id }
      expect(response).to redirect_to(movies_path)
    end

    it 'sets a flash notice after movie deletion' do
      delete :destroy, params: { id: movie.id }
      expect(flash[:notice]).to eq("Movie '#{movie.title}' deleted.")
    end
  end
end
