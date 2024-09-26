# frozen_string_literal: true

require 'rails_helper'

RSpec.describe Movie, type: :model do
  let(:movie_star_wars) { described_class.create(title: 'Star Wars', director: 'George Lucas') }
  let(:movie_thx) { described_class.create(title: 'THX-1138', director: 'George Lucas') }
  let(:movie_blade_runner) { described_class.create(title: 'Blade Runner', director: 'Ridley Scott') }

  after { described_class.destroy_all }

  describe 'with_director method' do
    let(:movies_by_lucas) { described_class.with_director('George Lucas') }

    it 'includes movies with the same director' do
      expect(movies_by_lucas).to include(movie_star_wars)
    end

    it 'includes other movies with the same director' do
      expect(movies_by_lucas).to include(movie_thx)
    end

    it 'does not include movies with different directors' do
      expect(movies_by_lucas).not_to include(movie_blade_runner)
    end
  end

  describe 'others_by_same_director method' do
    let(:other_movies_by_lucas) { movie_star_wars.others_by_same_director }

    it 'includes other movies by the same director' do
      expect(other_movies_by_lucas).to include(movie_thx)
    end

    it 'does not include the original movie in the result' do
      expect(other_movies_by_lucas).not_to include(movie_star_wars)
    end

    it 'does not include movies by different directors' do
      expect(other_movies_by_lucas).not_to include(movie_blade_runner)
    end
  end
end
