class MoviesController < ApplicationController
  before_action :set_movie, only: %i[ show edit update destroy ]

  # GET /movies or /movies.json
  def index
    session[:sort_by] = params[:sort_by] if params[:sort_by].present?
    session[:direction] = params[:direction] if params[:direction].present?

    sort_by = session[:sort_by] || 'title'
    direction = session[:direction] || 'asc'

    @movies = Movie.order("#{sort_by} #{direction}")
  end

  # GET /movies/1 or /movies/1.json
  def show
  end

  # GET /movies/new
  def new
    @movie = Movie.new
  end

  # GET /movies/1/edit
  def edit
  end

  def create
    @movie = Movie.new(movie_params)

    if @movie.save
      flash[:notice] = "#{@movie.title} was successfully created."
      redirect_to movies_path(sort_by: session[:sort_by], direction: session[:direction])
    else
      render 'new'
    end
  end

  def update
    @movie = Movie.find(params[:id])
    if @movie.update(movie_params)
      flash[:notice] = "#{@movie.title} was successfully updated."
      redirect_to movies_path(sort_by: session[:sort_by], direction: session[:direction])
    else
      render 'edit'
    end
  end

  # DELETE /movies/1 or /movies/1.json
  def destroy
    @movie = Movie.find(params[:id])
    @movie.destroy
    flash[:notice] = "#{@movie.title} was successfully deleted."
    redirect_to movies_path(sort_by: session[:sort_by], direction: session[:direction])
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_movie
      @movie = Movie.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def movie_params
      params.require(:movie).permit(:title, :rating, :description, :release_date)
    end
end
