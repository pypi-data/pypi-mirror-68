class Point < ActiveRecord::Base
  belongs_to :line # no need to set foreign key, model ok tablename not ok 
  validates :x, numericality: { only_integer: true }
  validates :y, numericality: { only_integer: true } 
end
