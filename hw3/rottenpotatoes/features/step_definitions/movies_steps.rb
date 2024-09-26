# frozen_string_literal: true

Given(/the following movies exist/) do |movies_table|
  movies_table.hashes.each do |movie|
    Movie.create!(movie)
  end
end

Then(/I should see "(.*)" before "(.*)"/) do |e1, e2|
  # Ensure that e1 occurs before e2 in the page content
  expect(page.body.index(e1)).to be < page.body.index(e2)
end

When(/I (un)?check the following ratings: (.*)/) do |uncheck, rating_list|
  rating_list.split(', ').each do |rating|
    step %(I #{uncheck ? 'un' : ''}check "ratings_#{rating}")
  end
end

Then(/I should see all the movies/) do
  # Make sure all movies in the database are visible on the page
  Movie.all.find_each do |movie|
    expect(page).to have_content(movie.title)
  end
end

When('I go to the edit page for {string}') do |movie_title|
  movie = Movie.find_by!(title: movie_title)
  visit edit_movie_path(movie)
end

When('I fill in {string} with {string}') do |field, value|
  fill_in field, with: value
end

When('I press {string}') do |button|
  click_on(button)
end

Then('the director of {string} should be {string}') do |movie_title, director_name|
  movie = Movie.find_by!(title: movie_title)
  expect(movie.director).to eq(director_name)
end

Given('I am on the details page for {string}') do |movie_title|
  movie = Movie.find_by!(title: movie_title)
  visit movie_path(movie)
end

When('I follow {string}') do |link|
  click_link link
end

Then('I should be on the Similar Movies page for {string}') do |movie_title|
  movie = Movie.find_by!(title: movie_title)
  expect(page).to have_current_path(similar_movies_path(movie))
end

Then('I should see {string}') do |text|
  expect(page).to have_content(text)
end

Then('I should not see {string}') do |text|
  expect(page).not_to have_content(text)
end

Then('I should be on the home page') do
  expect(page).to have_current_path(movies_path)
end
