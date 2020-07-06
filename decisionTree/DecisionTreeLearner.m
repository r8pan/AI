function [decisionTree] = decisionTreeLearner(X, Y, E)
	% Input:
	%	X, the list of features to be split on (word list)
	%	Y, output feature (1 or 2)
	%	E, dataSet (train Data)
	%
	% Output:
	%	A decision tree, with each row representing a node to be split
	%	each node would contain following information: wordId, which class gets split, point estimate of the unsplit one
	
	whos
	decisionTree = zeros(100, 4);
	pq = PriorityQueue(1);
        Entropy = 1;
	
	% expand 100 times
	for i = 1:100
		% iterate through all words as the feature
		  for j = length(X)
			dt = 0;
			dt1 = 0;
			df1 = 0;
			% iterate through all articles
			for k = 1:1061
				ind = E(:,1) == k;
                article = E(ind, :);
                [m n] = size(article);
				hasWord = 0;
				% iterate through the article for word
				for l = 1:m
					if article(l,2) == j
					%disp('found word in the article');
					    dt = dt + 1;
						hasWord = true;
                        if Y(k,1) == 1
							dt1 = dt1 + 1;
						end
					end
				end
				hasWord;
				if ~hasWord & Y(k) == 1
					df1 = df1 + 1;
				end
			end
		    df = 1061 - dt;
            dt2 = dt - dt1;
            df2 = df - df1;
						
            et = -(dt1/dt*log2(dt1/dt))-(dt2/dt*log2(dt2/dt))
            if isnan(et)
                et = 0;
            end
            ef = -(df1/df*log2(df1/df))-(df2/df*log2(df2/df))
            if isnan(ef)
                ef = 0;
            end
            % information gain
			ig = Entropy - 0.5 * (et + ef);
			if dt1 >= dt2
				ot = 1;
			else
				ot = 2;
			end
			if df1 >= df2
				of = 1;
			else
				of = 2;	  
			end
			
			pq.insert([ig, j, et, ef, ot, of]);
		
		end

		for s = 1:pq.size()
			  split = pq.remove();
	    end
		pq.clear();
        X{1,split(1,2)} = [];
		decisionTree(i, 1) = split(1, 2);
		if split(1,3) >= split(1,4)
			decisionTree(i, 2) = 1;
			decisionTree(i, 3) = split(1,6);
			Entropy = split(1,3);
		else
			decisionTree(i, 2) - 2;
			decisionTree(i, 3) = split(1, 5);
			Entropy = split(1,4);
		end

		
		
	end
	
	decisionTree

return
