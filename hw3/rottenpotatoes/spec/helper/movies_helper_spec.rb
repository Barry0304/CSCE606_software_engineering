require 'rails_helper'

RSpec.describe MoviesHelper, type: :helper do
  describe "#oddness" do
    it "returns 'odd' for odd numbers" do
      expect(helper.oddness(1)).to eq("odd")
      expect(helper.oddness(3)).to eq("odd")
    end

    it "returns 'even' for even numbers" do
      expect(helper.oddness(2)).to eq("even")
      expect(helper.oddness(4)).to eq("even")
    end
  end
end