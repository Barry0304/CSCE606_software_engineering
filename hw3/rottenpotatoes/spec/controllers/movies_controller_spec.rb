require 'rails_helper'

RSpec.describe MoviesController, type: :controller do
  before(:all) do
    Movie.destroy_all

    Movie.create( title: "Big Hero 6",
                  rating: "PG",
                  release_date: "2014-11-07",
                  director: "Don Hall, Chris Williams")

    Movie.create(title: "Inception", rating: "PG-13", release_date: "2010-07-16", director: "Christopher Nolan")
    Movie.create(title: "Interstellar", rating: "PG-13", release_date: "2014-11-07", director: "Christopher Nolan")
    Movie.create(title: "Alien", rating: "R", release_date: "1979-05-25", director: "Ridley Scott")
    Movie.create(title: "Blade Runner", rating: "R", release_date: "1982-06-25", director: "Ridley Scott")
                
  end

  describe "when trying to find movies by the same director" do
    it "returns a valid collection when a valid director is present" do
      movie = Movie.create(title: "Inception", director: "Christopher Nolan")
      movie2 = Movie.create(title: "Interstellar", director: "Christopher Nolan")
      get :find_similar, params: { id: movie.id }
      expect(assigns(:similar_movies)).to include(movie2)
    end
  
    it "redirects to index with a warning when no director is present" do
      movie = Movie.create(title: "Unknown Movie", director: nil)
      get :find_similar, params: { id: movie.id }
      expect(response).to redirect_to(movies_path)
      expect(flash[:notice]).to match(/has no director info/)
    end
  end
  

  describe "creates" do
    it "movies with valid parameters" do
      get :create, params: {movie: {title: "Threenagers", director: "The Prof.s Ritchey",
                    rating: "G", release_date: "2015-01-20"}}
      expect(response).to redirect_to movies_path
      expect(flash[:notice]).to match(/Threenagers was successfully created./)
      Movie.find_by(title: "Threenagers").destroy
    end
  end

  describe 'updates' do
    it "redirects to the movie details page and flashes a notice" do
      movie = Movie.create(title: 'Attack of the Munchkins', director: 'Sofia Grace',
                           rating: 'PG', release_date: '2024-08-19')
      get :update, params: {
        id: movie.id,
        movie: {
          description: 'A whimsical and adventurous film where a small town is unexpectedly '\
          'overrun by mischievous, pint-sized creatures known as Munchkins. As the townspeople ' \
          'scramble to defend their homes and livelihoods, they uncover the Munchkins\' origins ' \
          'and intentions. With humor and heart, the community bands together, discovering ' \
          'hidden strengths and forging new friendships along the way. The movie blends comedy, ' \
          'action, and a touch of fantasy, offering a light-hearted yet thrilling experience ' \
          'for audiences of all ages.'}
        }

      expect(response).to redirect_to movie_path(movie)
      expect(flash[:notice]).to match(/Attack of the Munchkins was successfully updated./)
      movie.destroy
    end

    it "actually does the update" do
      movie = Movie.create(title: 'Seven Samurai', director: 'Yasujiro Ozu',
                           rating: 'PG', release_date: '1954-04-26')
      get :update, params: { id: movie.id, movie: { director: 'Akira Kurosawa' } }

      expect(assigns(:movie).director).to eq('Akira Kurosawa')
      movie.destroy
    end
  end
  
  describe "GET find_similar" do
    it "finds movies by the same director" do
      movie = Movie.create(title: "Alien", director: "Ridley Scott")
      movie2 = Movie.create(title: "Blade Runner", director: "Ridley Scott")
      get :find_similar, params: { id: movie.id }
      expect(assigns(:similar_movies)).to include(movie2)
    end

    it "redirects to index with a warning when no director is present" do
      movie = Movie.create(title: "Alien", director: nil)
      get :find_similar, params: { id: movie.id }
      expect(response).to redirect_to(movies_path)
      expect(flash[:notice]).to match(/has no director info/)
    end
  end

  describe 'DELETE destroy' do
    it "deletes the movie and redirects to the movies index with a notice" do
      movie = Movie.create(title: 'Test Movie', director: 'Test Director', rating: 'PG', release_date: '2024-01-01')
      expect {
        delete :destroy, params: { id: movie.id }
      }.to change(Movie, :count).by(-1)
      expect(response).to redirect_to(movies_path)
      expect(flash[:notice]).to eq("Movie '#{movie.title}' deleted.")
    end
  end  

end

