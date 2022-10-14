clear all
disp('Trilateral Measurement')
x=[5 35 53];
y=[41 10 30];%the known position of sensor
plot(x,y,'o');
axis([-5 65 -5 65]);
hold on
[x0,y0]=ginput(3);
plot(x0,y0,'g:o')
axis([-5 65 -5 65])

distance= zeros(3,3);
for i=1:3
    for j=1:3
    distance(i,j) = sqrt((x(i)-x0(j))^2 + (y(i)-y0(j))^2);
    end
end
error=0; %rand(1,3)-0.3
% error=rand(3,3)-0.3;
distance=distance-distance.*(error/7);      %error control
aa = zeros(2,2,3);
bb = zeros(2,1,3);
cc = zeros(1,2,3);
for h=1:3
    aa(:,:,h)=inv(2*([x(1)-x(3) y(1)-y(3);x(2)-x(3) y(2)-y(3)]));
    bb(:,:,h)=[x(1)^2-x(3)^2+y(1)^2-y(3)^2+distance(3,h)^2-distance(1,h)^2;x(2)^2-x(3)^2+y(2)^2-y(3)^2+distance(3,h)^2-distance(2,h)^2];
    cc(:,:,h)=(aa(:,:,h)*bb(:,:,h))'; %compute the location and store position
    plot(cc(:,1,h),cc(:,2,h),'+')%plot the cross points
    axis([-50 100 -50 100])
    %e(j)=sqrt((cc(j,1)-x0)^2+(cc(j,2)-y0)^2) 
   circle(distance(1,h),x(1),y(1),'r');
   circle(distance(2,h),x(2),y(2),'b');
   circle(distance(3,h),x(3),y(3),'cyan');
   plot([x(1),cc(1,1,h)],[y(1),cc(1,2,h)],'k');
   plot([x(2),cc(1,1,h)],[y(2),cc(1,2,h)],'k');
   plot([x(3),cc(1,1,h)],[y(3),cc(1,2,h)],'k');
   axis equal;
end
s='Trilateral Measurement'           
title(s)
hold on
% figure
% rate=1:1:7;
% plot(rate,e,'g:*')
% xlabel('x/Error Rate') %xlabel,x-l-a-b-e-l
% ylabel('y/Error Rate')
% axis([0 7 -20 50])
% hold on
