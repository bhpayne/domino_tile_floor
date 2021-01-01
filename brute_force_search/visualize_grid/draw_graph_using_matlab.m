# octave

setenv("GNUTERM","qt"); # for mac

# read in a CSV containing the snake location
this_grid=csvread('4x3.csv');

# determine the size of the grid
num_rows = size(this_grid,1);
num_cols = size(this_grid,2);

# initialize an array to hold the values of the row,col per index
ary_of_indices_and_locations=zeros(num_rows*num_cols,2);

# for each index, determine the row,col
for indx = 1:(num_rows*num_cols)
  for this_row = 1:num_rows
    if (sum(this_grid(this_row,:)==indx)==1)
      ary_of_indices_and_locations(indx,1)=this_row;
    endif
  end
  for this_col = 1:num_cols
    if (sum(this_grid(:,this_col)==indx)==1)
      ary_of_indices_and_locations(indx,2)=this_col;
    endif
  end
end

# display array in terminal
#ary_of_indices_and_locations

# draw the snake
figure; 
for indx = 1:(num_rows*num_cols-1)
#  figure; 
  plot([ary_of_indices_and_locations(indx,  2) ary_of_indices_and_locations(indx+1,  2)],...
       [(num_rows+1)-ary_of_indices_and_locations(indx,1) (num_rows+1)-ary_of_indices_and_locations(indx+1,1)],...
       'linewidth',5,'color','red'); hold on;
#  title([num2str(indx) ': ' num2str(ary_of_indices_and_locations(indx,  2)) ...
#                        ',' num2str((num_rows+1)-ary_of_indices_and_locations(indx,  1)) ...
#                     ' to ' num2str(ary_of_indices_and_locations(indx+1,2)) ... 
#                        ',' num2str((num_rows+1)-ary_of_indices_and_locations(indx+1,1)) ]);
end

saveas (gcf, "snake.png");
