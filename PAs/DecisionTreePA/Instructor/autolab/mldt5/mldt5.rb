require "AssessmentBase.rb"

module Mldt5
  include AssessmentBase

  def assessmentInitialize(course)
    super("mldt5",course)
    @problems = []
  end

end
