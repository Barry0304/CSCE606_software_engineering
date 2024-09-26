# frozen_string_literal: true

# Represents movies in the database and provides methods
# to query movies based on their director.
class Movie < ActiveRecord::Base
  def self.with_director(director)
    where(director:)
  end

  def others_by_same_director
    Movie.where(director:).where.not(id:)
  end
end
