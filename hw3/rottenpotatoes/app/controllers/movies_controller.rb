# frozen_string_literal: true

# Handles actions related to movies, such as listing, creating, and deleting.
class MoviesController < ApplicationController
  before_action :set_movie, only: %i[show edit update destroy find_similar]

  def show
    # Movie is set by the set_movie before_action callback
    # render 'show' template by default
  end

  def index
    @movies = Movie.all
  end

  def new
    # default: render 'new' template
  end

  def create
    @movie = Movie.create!(movie_params)
    flash[:notice] = "#{@movie.title} was successfully created."
    redirect_to movies_path
  end

  def edit
    # Movie is set by the set_movie before_action callback
  end

  def update
    # Movie is set by the set_movie before_action callback
    @movie.update!(movie_params)
    flash[:notice] = "#{@movie.title} was successfully updated."
    redirect_to movie_path(@movie)
  end

  def destroy
    # Movie is set by the set_movie before_action callback
    @movie.destroy
    flash[:notice] = "Movie '#{@movie.title}' deleted."
    redirect_to movies_path
  end

  def find_similar
    # Movie is set by the set_movie before_action callback
    director = @movie.director
    if director.blank?
      redirect_to movies_path, notice: "'#{@movie.title}' has no director info"
    else
      @similar_movies = Movie.where(director:).where.not(id: @movie.id)
    end
  end

  private

  # Making "internal" methods private is not required, but is a common practice.
  # This helps make clear which methods respond to requests, and which ones do not.
  def movie_params
    params.require(:movie).permit(:title, :rating, :description, :release_date, :director)
  end

  # Callback to set movie for the actions that require it
  def set_movie
    @movie = Movie.find(params[:id])
  end
end
