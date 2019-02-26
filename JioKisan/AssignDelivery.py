import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JioKisan.settings')

import django
django.setup()

from trucks.models import Driver,Delivery
import numpy as np




def initializeMappingList(num_drivers, num_consignments, drivers, consignments):

    # A list of dicts map indices of driver/pickup/drop  
    mappingList = []
    for i in range(num_drivers+2*num_consignments):
        if(i<num_drivers):
            entryType = 'Driver'
            pk = drivers[i].pk
            address = str(drivers[i].currentPositionLatitude)+','+str(drivers[i].currentPositionLongitude) 
            weight = drivers[i].truckCapacity
        else:
            k=i-num_drivers
            consignmentEntry_index = int(k/2)

            if(k%2==0):
                entryType = 'Pickup Location'
                pk = consignments[consignmentEntry_index].pk
                address = str(consignments[consignmentEntry_index].pickupLocationLatitude) + ',' + str(consignments[consignmentEntry_index].pickupLocationLongitude)

            else:
                entryType = 'Drop Location'
                pk = consignments[consignmentEntry_index].pk
                address = str(consignments[consignmentEntry_index].dropLocationLatitude) + ',' + str(consignments[consignmentEntry_index].dropLocationLongitude)

            weight = consignments[consignmentEntry_index].weight
            
        infoDict = {
            'entryType' : entryType,
            'pk' : pk,
            'address' : address,
            'weight' : weight
        } 

        mappingList.append(infoDict)
        
    return mappingList



def fillDistanceMatrix(originList, destinationList):
    
    distanceMatrix = np.random.randint(1,15,size=(len(destinationList),len(originList)))
    
    maxValue = np.max(distanceMatrix)
    
    
    for i in originList:
        if i['entryType'] == 'Driver':
            for j in destinationList:
                if (j['entryType'] == 'Pickup Location') and (j['weight']>i['weight']):
                    distanceMatrix[destinationList.index(j)][originList.index(i)] = maxValue + 1
                    
                    
    
    return distanceMatrix




def driverDeliveryAssignment(mappingList, num_drivers, num_consignments):
    # This List will Contain indexes of location in mappingList and in order for driver has to go 
    locations = []
    assignedConsignments_num = 0
    # A list dictionaries like info dict containing only pickup location parts of assigned consignments
    assignedConsignments = []  
    
    originList = [ mappingList[i] for i in range(num_drivers) ]
    destinationList = [ mappingList[i] for i in range(num_drivers, len(mappingList), 2) ]
 
    
    for i in originList:
        if i['entryType']!='Driver':
            print('Something Wrong in Origin List')
            
    
    for i in destinationList:
        if i['entryType']!='Pickup Location':
            print('Something Wrong in Destination List')
    
    
       
    # Origins are along column & destinations are along rows
#     distanceMatrix = np.zeros(shape=(len(destinationList),len(originList)))
    
    #Compute Distances 
    distanceMatrix = fillDistanceMatrix(originList, destinationList) 
    

    firstPickup_index = np.where(distanceMatrix == np.min(distanceMatrix))[0][0] 
    firstDriver_index =  np.where(distanceMatrix == np.min(distanceMatrix))[1][0]
    
    firstPickup = destinationList[firstPickup_index]
    
    firstDriver = originList[firstDriver_index]
    

    #    let myDriver be a driver object from django model while 
    #   firstDriver is dictionary containing details about myDriver including pk    
    
    #  Make this driver hired.
   
    assignedConsignments_num = 1
    locations.append(firstPickup)
    
    
    loadedWeight = firstPickup['weight']
    
    # print('Got the first pickup loaded weight is ', loadedWeight, 'truck weight is ', firstDriver['weight'])
    
    originList = []
    originList.append(firstPickup)
    destinationList.remove(firstPickup)
    destinationList.append(mappingList[mappingList.index(firstPickup)+1])
    assignedConsignments.append(firstPickup)
    
    
    
    
    while(len(destinationList)>0):
    
        # We have to filter left consignments according to truck capacity or further filters can be added here
        # An example of another filter may me to remove consignments with different crop
        removeIndices = []
        for i in destinationList:
            if i['entryType'] == 'Pickup Location':   # A drop location might still be in destination list
                if loadedWeight + i['weight'] > firstDriver['weight']:
                    removeIndices.append(i)      # Remove Delivery with more weight
        for i in removeIndices:
            destinationList.remove(i)
                    
        
        
        
        distanceMatrix = fillDistanceMatrix(originList, destinationList)
        
        
        nextLocation_index = firstPickup_index = np.where(distanceMatrix == np.min(distanceMatrix))[0][0]
    
        nextLocation = destinationList[nextLocation_index]
        
        destinationList.remove(nextLocation)
        
        
        
        if(nextLocation['entryType'] == 'Pickup Location'):
            assignedConsignments_num = assignedConsignments_num + 1
            if(assignedConsignments_num<6):
                loadedWeight = loadedWeight + nextLocation['weight']
                assignedConsignments.append(nextLocation)
                locations.append(nextLocation)
                destinationList.append(mappingList[mappingList.index(nextLocation)+1])
        
        else:
            locations.append(nextLocation)
            
    
    
    return firstDriver, locations, assignedConsignments



def getDrivers():
    # Drivers which are not hired and add further filters
    drivers = Driver.objects.all().filter(hired=False)

    return drivers

def getConsignments():
    # Consignments which are pending
    consignments = Delivery.objects.all().filter(status="PENDING") # ADD FURTHER FILTERS LIKE PICKUP date if required
    
    return consignments

def mapConsignments():
    
    # Consignments which are pending
    drivers = getDrivers()
    consignments = getConsignments()
    num_drivers = drivers.count()
    num_consignments = consignments.count()

    # A list of dicts map indices of driver/pickup/drop 

    while( (num_drivers>0) and (num_consignments>0) ):
        mappingList = initializeMappingList(num_drivers, num_consignments, drivers, consignments)
        assignedDriver , pathOfDriver, assignedConsignments = driverDeliveryAssignment(mappingList, num_drivers, num_consignments)

        # Now we have to change hired status of driver and status of consignments

        assignedDriverObject = Driver.objects.get(pk = assignedDriver['pk'])
        assignedDriverObject.hired = True


        # attention
        # attention
        # !!!!! We have to add pathOfDriver to driver model object
        # attention
        # attention



        for entry in assignedConsignments:
            consignmentObject = Delivery.objects.get(pk = entry['pk'])
            consignmentObject.status = "ASSIGNED"

        drivers = getDrivers()
        consignments = getConsignments()
        num_drivers = drivers.count()
        num_consignments = consignments.count()

