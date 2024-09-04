def sum(arr)
	arr.sum
end

def max_2_sum(arr)
	return 0 if arr.empty?
	return arr[0] if arr.length == 1
	return arr.max(2).sum
end

def sum_to_n?(arr, num)
	return false if arr.empty?
	have = false
	arr.each do |e|
		have = have || (arr.include?(num - e) && ((num - e)!=e)) 
	end
	return have
end

def hello(str)
	return "Hello, #{str}"
end

def starts_with_consonant?(string)
	return false if string.empty?  # 檢查字串是否為空
	return !!(string[0] =~ /^[b-df-hj-np-tv-zB-DF-HJ-NP-TV-Z]/)
end

def binary_multiple_of_4?(string)
	return false unless string.match?(/\A[01]+\z/)
	string.to_i(2) % 4 == 0
end

class BookInStock
	attr_accessor :isbn, :price

	def initialize(isbn, price)
		raise ArgumentError, 'ISBN cannot be empty' if isbn.empty?
		raise ArgumentError, 'Price must be greater than zero' if price <= 0
		@isbn = isbn
		@price = price
	end

	def price_as_string
		format('$%.2f', @price)
	end
end