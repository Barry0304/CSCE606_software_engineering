module MoviesHelper
  def toggle_direction(column)
    if session[:sort_by] == column && params[:commit].blank? # 確保只有在使用者未提交表單時才切換方向
      session[:direction] == 'asc' ? 'desc' : 'asc'
    else
      'asc'
    end
  end

  def sort_icon(column)
    if session[:sort_by] == column
      session[:direction] == 'asc' ? '▲' : '▼'
    else
      ''
    end
  end
end
