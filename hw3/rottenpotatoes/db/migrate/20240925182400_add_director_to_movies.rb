class AddDirectorToMovies < ActiveRecord::Migration[7.2]
  def change
    add_column :movies, :director, :string
  end
end
