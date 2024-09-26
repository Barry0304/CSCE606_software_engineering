# frozen_string_literal: true

require 'rails_helper'

RSpec.describe MoviesHelper, type: :helper do
  describe '#oddness' do
    it "returns 'odd' for the number 1" do
      expect(helper.oddness(1)).to eq('odd')
    end

    it "returns 'odd' for the number 3" do
      expect(helper.oddness(3)).to eq('odd')
    end

    it "returns 'even' for the number 2" do
      expect(helper.oddness(2)).to eq('even')
    end

    it "returns 'even' for the number 4" do
      expect(helper.oddness(4)).to eq('even')
    end
  end
end
