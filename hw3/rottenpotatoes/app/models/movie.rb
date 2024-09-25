class Movie < ActiveRecord::Base

  def self.with_director(director)
    where(director: director)
  end

  def others_by_same_director
    Movie.where(director: self.director).where.not(id: self.id)
  end
  
end