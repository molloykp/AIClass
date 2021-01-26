require "AssessmentBase.rb"

module AiALSearch
  include AssessmentBase

  def assessmentInitialize(course)
    super("aiALSearch",course)
    @problems = []
  end

end
