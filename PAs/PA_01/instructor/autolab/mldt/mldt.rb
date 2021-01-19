require "AssessmentBase.rb"

module Mldt
  include AssessmentBase

  def assessmentInitialize(course)
    super("mldt",course)
    @problems = []
  end

end
