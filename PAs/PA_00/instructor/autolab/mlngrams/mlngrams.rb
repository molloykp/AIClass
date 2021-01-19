require "AssessmentBase.rb"

module Mlngrams
  include AssessmentBase

  def assessmentInitialize(course)
    super("mlngrams",course)
    @problems = []
  end

end
