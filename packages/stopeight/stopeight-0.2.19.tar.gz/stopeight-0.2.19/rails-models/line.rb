class Line < ActiveRecord::Base
  self.table_name = 'slines'
  has_many :points, dependent: :destroy

#  def self.before_destroy
#    @points = Point.find(:all, :conditions=>{ :line_id=>self.id })
#    @points.each do |p|
#      p.destroy
#    end
#  end
end
