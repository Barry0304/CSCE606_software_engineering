require 'rails_helper'

RSpec.describe Movie, type: :model do
  before(:all) do
    @movie1 = Movie.create(title: "Star Wars", director: "George Lucas")
    @movie2 = Movie.create(title: "THX-1138", director: "George Lucas")
    @movie3 = Movie.create(title: "Blade Runner", director: "Ridley Scott")
  end

  after(:all) do
    Movie.destroy_all
  end

  describe "with_director method" do
    it "returns movies with the same director" do
      movies = Movie.with_director("George Lucas")
      expect(movies).to include(@movie1, @movie2)
      expect(movies).not_to include(@movie3)
    end
  end

  describe "others_by_same_director method" do
    it "returns other movies by the same director" do
      other_movies = @movie1.others_by_same_director
      expect(other_movies).to include(@movie2)
      expect(other_movies).not_to include(@movie1, @movie3)
    end

    it "does not return movies by different directors" do
      other_movies = @movie1.others_by_same_director
      expect(other_movies).not_to include(@movie3)
    end
  end
end