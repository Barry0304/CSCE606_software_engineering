# frozen_string_literal: true

require_relative '../lib/ruby_intro'

# rubocop:disable Metrics/BlockLength
describe 'Ruby intro part 3' do
  describe 'BookInStock' do
    it 'should be defined' do
      expect { BookInStock }.not_to raise_error
    end

    describe 'getters and setters' do
      before(:each)  { @book = BookInStock.new('isbn1', 33.8) }
      it 'should set ISBN', points: 3 do
        expect(@book.isbn).to eq('isbn1')
      end
      it 'should set price', points: 3 do
        expect(@book.price).to eq(33.8)
      end
      it 'should be able to change ISBN', points: 4 do
        @book.isbn = 'isbn2'
        expect(@book.isbn).to eq('isbn2')
      end
      it 'should be able to change price', points: 4 do
        @book.price = 300.0
        expect(@book.price).to eq(300.0)
      end
    end
    describe 'constructor' do
      it 'should reject invalid ISBN number', points: 3 do
        expect { BookInStock.new('', 25.00) }.to raise_error(ArgumentError)
      end
      it 'should reject zero price', points: 3 do
        expect { BookInStock.new('isbn1', 0) }.to raise_error(ArgumentError)
      end
      it 'should reject negative price', points: 3 do
        expect { BookInStock.new('isbn1', -5.0) }.to raise_error(ArgumentError)
      end
    end
    describe '#price_as_string' do
      it 'should be defined' do
        expect(BookInStock.new('isbn1', 10)).to respond_to(:price_as_string)
      end
      it 'should display 33.95 as $33.95', points: 3 do
        expect(BookInStock.new('isbn1', 33.95).price_as_string).to eq('$33.95')
      end
      it 'should display 1.1 as $1.10', points: 4 do
        expect(BookInStock.new('isbn1', 1.1).price_as_string).to eq('$1.10')
      end
      it 'should display 20 as $20.00', points: 4 do
        expect(BookInStock.new('isbn1', 20).price_as_string).to eq('$20.00')
      end
    end
  end
end
# rubocop:enable Metrics/BlockLength
